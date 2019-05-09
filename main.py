# -*- coding: utf-8 -*-
import sys
import zipfile
import os.path
import glob
import xml.etree.ElementTree as et
import numpy as np 
import gdal
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.Qt import QApplication, QEventLoop, QCursor
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from form import Ui_Dialog

class Form(QtWidgets.QDialog):

    def __init__(self,parent=None):
        super(Form, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def LoadFolderSelect(self):
        path = QFileDialog.getExistingDirectory(None, "", "")
        self.ui.LoadFolderPath.setText(path)

    def accept(self):
        folder = self.ui.LoadFolderPath.text()

        if not (os.path.exists(folder) and (os.path.isdir(folder))):
            QtWidgets.QMessageBox.information(None, "エラー", "指定したフォルダ「" + folder + "」が見つかりませんでした。", QMessageBox.Ok)
            return

        filelist = glob.glob(folder + "\*.zip")
        if len(filelist) == 0:
            QtWidgets.QMessageBox.information(None, "エラー", "zipファイルは見つかりませんでした。", QMessageBox.Ok)
            return

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            for z in filelist:
                with zipfile.ZipFile(z, 'r') as zf:
                    decomp = zf.namelist()
                    if len(decomp) == 0:
                        self.ui.LogViewer.append("「" + zipfilename + "」内にファイルが見つかりませんでした。")
                        continue
                    for dfile in decomp:
                        with zf.open(dfile, 'r') as file:
                            gmldem = JpGisGML()
                            text = file.read().decode('utf_8')
                            gmldem.ReadText(text)
                            gmldem.ToGeoTiff(folder)

                        self.ui.LogViewer.append(dfile + " :終了")
                        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
        finally:
            QApplication.restoreOverrideCursor()
            QtWidgets.QMessageBox.information(None, "終了", "終了しました。", QMessageBox.Ok)

class JpGisGML :
#    __ns = {}
#    __dem = np.zeros([0, 0])
#    __ncol = 0
#    __nrow = 0
#    __xllcorner = 0.0
#    __yllcorner = 0.0
#    __cellsize = 0.0
#    __nodata = -9999
#    __meshcode = ""

    def __init__(self) :
        self.__ns = {
            'ns' : 'http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema',
            'gml' : 'http://www.opengis.net/gml/3.2',
            'xsi' : 'http://www.w3.org/2001/XMLSchema-instance',
            'xlink' : 'http://www.w3.org/1999/xlink'
        }
        self.__nodata = -9999
    def ReadText(self, text) :
        root = et.fromstring(text)
        dem = root.find('ns:DEM', self.__ns)
        mesh = dem.find('ns:mesh', self.__ns)
        coverage = dem.find('ns:coverage', self.__ns)
        envelope = coverage.find('gml:boundedBy//gml:Envelope', self.__ns)
        grid = coverage.find('gml:gridDomain//gml:Grid//gml:limits//gml:GridEnvelope', self.__ns)
        gridfunc = coverage.find('gml:coverageFunction//gml:GridFunction', self.__ns)
        rule = gridfunc.find('gml:sequenceRule', self.__ns)

        #メッシュコード
        self.__meshcode = mesh.text

        #左下、右上の座標取得
        str = envelope.find('gml:lowerCorner', self.__ns).text.split(' ')
        self.__yllcorner, self.__xllcorner = float(str[0]),float(str[1])
        str = envelope.find('gml:upperCorner', self.__ns).text.split(' ')
        self.__yucorner, self.__xucorner = float(str[0]),float(str[1])

        #行、列数取得
        str = grid.find('gml:low', self.__ns).text.split(' ')
        lowx,lowy = int(str[0]),int(str[1])
        str = grid.find('gml:high', self.__ns).text.split(' ')
        highx,highy = int(str[0]),int(str[1])
        self.__ncol = highx - lowx + 1
        self.__nrow = highy - lowy + 1

        #セルサイズ
        self.__cellsize_x = (self.__xucorner - self.__xllcorner) / self.__ncol
        self.__cellsize_y = (self.__yucorner - self.__yllcorner) / self.__nrow

        #標高値取得
        self.__dem = np.zeros([self.__nrow, self.__ncol])
        self.__dem.fill(self.__nodata)
        str = gridfunc.find('gml:startPoint', self.__ns).text.split(' ')
        x,y = int(str[0]), int(str[1])
        datapoints = coverage.find('gml:rangeSet//gml:DataBlock//gml:tupleList', self.__ns).text.splitlines()
        for datapoint in datapoints:
            str = datapoint.split(',')
            if len(str) == 1: continue
            desc,value = str[0],np.float64(str[1])
            if (desc == '地表面') or (desc == '表層面') or (desc == 'その他'):
                self.__dem[y][x] = value
            x += 1
            if x > highx:
                x = 0
                y += 1
            if y > highy:
                break

    def ToGeoTiff(self, savefoldername) :
        savetiffilename = savefoldername + "\\"+ self.__meshcode + ".tif"

        driver = gdal.GetDriverByName("GTiff")
        dst_ds = driver.Create(savetiffilename, self.__ncol, self.__nrow, 1, gdal.GDT_Float32, [])
        dst_ds.SetProjection('GEOGCS["JGD2000",DATUM["Japanese_Geodetic_Datum_2000",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY["EPSG","6612"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4612"]]')
        geotransform = [self.__xllcorner, self.__cellsize_x, 0, self.__yucorner, 0, -self.__cellsize_y]
        dst_ds.SetGeoTransform(geotransform)
        rband = dst_ds.GetRasterBand(1)
        rband.WriteArray(self.__dem)
        rband.SetNoDataValue(self.__nodata)
        dst_ds.FlushCache()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Form()
    window.show()
    sys.exit(app.exec_())
