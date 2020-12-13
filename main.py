#!/usr/bin/python3

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/jbd/qt_proj/Dredging/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

""" pyinstaller --windowed myapp.py
# cd dist/myapp.app/Contents/MacOs
# mkdir tcl tk
# cp -R /Library/Frameworks/Python.framework/Versions/3.7/lib/tcl* tcl/
# cp -R /Library/Frameworks/Python.framework/Versions/3.7/lib/tk* tk/
"""


from fbs_runtime.application_context.PyQt5  import ApplicationContext


import matplotlib
matplotlib.use('QT5Agg')
from matplotlib.figure import Figure
from os.path import expanduser
from concurrent.futures import ThreadPoolExecutor,wait

import pandas as pd
from matplotlib import style
style.use('ggplot')
# import matplotlib.pyplot as plt
import sqlite3
from dateutil.parser import parse as parse_time
import csv
# from sqlalchemy import sql
# import pyqtgraph as pg
import numpy as np
# from PyQt5.QtWidgets import  QSizePolicy
# import multiprocessing
# import inspect
import threading



from scipy import signal


from PyQt5 import QtCore, QtGui, QtWidgets,QtGui


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import os

import time
# import asyncio
# from multiprocessing import Process




class Dredging(object):

    def load_data(self,url=None,filePath=None):
        try:
            if url:

                self.dredging_df = pd.read_csv(url)
            elif filePath:
                self.dredging_df = pd.read_csv(filePath)


            self.dredging_df = self.dredging_df[
                ['Time', 'BucketX', 'BucketY', 'BucketZ', 'BucketHdg', 'BoomAng',
                 'StickAng', 'BucketAng', 'Tide', 'BargeX', 'BargeY', 'BargeHdg',
                 'CraneDepth', 'CraneAngle', 'CraneLength', 'BoomLength', 'CabinX',
                 'CabinY', 'CabinZ', 'CabinHdg', 'DredgeZ', 'SurveyZ', 'DesignZ',
                 ]]
            self.dredging_df_out = self.dredging_df.copy()


            # self.dredging_df_out.loc[:, "time closed bucket"] = self.dredging_df_out["BOpwtrsfc"]
            # self.dredging_df_out['time closed bucket'] = "close"
            self.dredging_df['Time'] = pd.to_datetime(self.dredging_df['Time'])
            self.dredging_df = self.dredging_df.set_index('Time')
            self.dredging_df['Time'] = self.dredging_df.index

            # self.dredging_df_out.to_csv(os.path.join(current_dir,"report1.csv"))


        except EOFError as err:

            print(err)

    def report_creat(self):


        self.dredging_df_out['moveX'] = round(self.dredging_df_out['BucketX'] - \
                                              self.dredging_df_out['BargeX'], 2)
        self.dredging_df_out['moveY'] = round(self.dredging_df_out['BucketY'] - \
                                              self.dredging_df_out['BargeY'], 2)

        self.max_bucket = 47

        self.creat_report()
        # self.dredging_df['Time'] = pd.to_datetime(self.dredging_df['Time'])
        # self.dredging_df = self.dredging_df.set_index('Time')
        # self.dredging_df['Time'] = self.dredging_df.index

        self.dredging_df_out['Time'] = pd.to_datetime(self.dredging_df_out['Time'])
        self.dredging_df_out = self.dredging_df_out.set_index('Time')
        self.dredging_df_out['Time'] = self.dredging_df_out.index


    def bucket_to_weter(self):
        # 0.54x as 1/(average rozmah/(average cycle time/2))
        time_coef = 1/(self.averagerozmah/(self.average_time_cucle/2))


        self.dredging_df_out.loc[:, ("BucketOWS/VDT")] = self.dredging_df_out["BucketZ"]
        self.dredging_df_out.loc[self.dredging_df_out["BucketOWS/VDT"] < 0, "Bucket_w_s"] = np.nan
        self.dredging_df_out.loc["BucketOWS/VDT"] = self.max_buccketZ - self.dredging_df_out["BucketOWS/VDT"]


        # self.dredging_df_out.loc[:, ("BucketOWS/VDT")] = round(self.dredging_df_out["BucketZ"] * time_coef, 2)

        self.dredging_df_out.loc[:, ("Bucket_w_s")] = self.dredging_df_out["BucketZ"]
        self.dredging_df_out.loc[:, ("Bucket_w_s")] = round(self.dredging_df_out["BucketZ"] * time_coef, 2)
        self.dredging_df_out.loc[self.dredging_df_out["BucketZ"] < 0,"Bucket_w_s"] = np.nan

        # self.dredging_df_out[['BucketOWS/VDT','BucketZ','Bucket_w_s']].to_csv('/Users/jbd/PycharmProjects/Dredging/out_new.csv')

    def diff_bar(self):
        self.dredging_df_out['diff BucketZ'] = self.dredging_df_out['BucketZ'].diff(periods=25)

        # Dredging_.dredging_df['vector of z'] = Dredging_.dredging_df['diff BucketZ']

        self.dredging_df_out.loc[:, "vector of z"] = self.dredging_df_out['diff BucketZ']
        self.dredging_df_out.loc[self.dredging_df_out.loc[:, "vector of z"] > 0.1, 'vector of z'] = 1
        self.dredging_df_out.loc[self.dredging_df_out.loc[:, "vector of z"] < -0.1, 'vector of z'] = -1
        self.dredging_df_out.loc[self.dredging_df_out.loc[:, "vector of z"] == 0, 'vector of z'] = np.NAN

        # min_peakind_index,max_peakind_index = closet_position(Dredging_.dredging_df['vector of z'])

        self.dredging_df_out.loc[:, "vector of z piec"] = self.dredging_df_out['vector of z'].diff()
        self.dredging_df_out.loc[(self.dredging_df_out.loc[:, "vector of z piec"] < -1) & (
                self.dredging_df_out.loc[:, "BucketZ"] > 45), 'vector of z piec'] = 1
        # Dredging_.dredging_df.loc[Dredging_.dredging_df.loc[:, "vector of z"] < -0.1,'vector of z'] = -1
        self.dredging_df_out.loc[self.dredging_df_out.loc[:, "vector of z piec"] >= -1, 'vector of z piec'] = np.NAN



    def creat_report(self):



        #output
        # 1 Average Cycle time /sec
        # 2 Number of buckets (number of bucket grabs taken)
        # 3 Bucket open to the water surface /vertical distance traveled
        # 4 Average bucket closure depth (average bucketZ at closure)
        self.calculateaverage()
        # 5 Bucket open to the water surface /secs
        self.bucket_to_weter()

        # 6 Bucket open to the water surface /vertical distance traveled
        # 7 Bucket open to the water surface /angle swung



        # self.closet_position()

    def statistics_series(self,data,start=0,fin=None,step=1):
        serries = pd.Series(data[start:fin])

        #len(serries), serries.min(), serries.max()
        return serries.describe(include='all')


    def calcucate_cycle(self):
        BucketHdg = self.dredging_df[['BucketZ','BoomAng']]

    def visualize(self,data=None,x_=None,y_=None,start=0,fin=None):
        style.use('ggplot')
        if x_:
            self.dredging_df[start:fin].plot(x=x_,y=y_)
        elif data:
            self.dredging_df[x_].plot()
        # plt.show()


    def callculate_Average_cucle_time(self,start=0,fin=None):
        boomAng = np.array(self.dredging_df[start:fin][''])
        if fin:
            period = fin-start
        else:
            period = len(self.dredging_df)+1
        self.min_peakinds = len(signal.find_peaks_cwt(boomAng, np.arange(1, 1000)))



        return round(period/self.min_peakinds,4)


    def calculateaverage(self):

        bucket_analyse = []

        lenght = len(self.dredging_df)
        lenght_diff = int(lenght/24)



        for i in range(1,25):
            data = self.dredging_df[(i-1)*lenght_diff:i*lenght_diff]["BucketZ"]
            arr = np.array(data)
            ab_s, quantity,average_down_position,average_distantion = self.quantityAverage(arr)

            bucket_analyse.append([i,ab_s, quantity,average_down_position,average_distantion])
        # output
        # 1 Average Cycle time /sec
        # 2 Number of buckets (number of bucket grabs taken)
        # 3 Bucket open to the water surface /vertical distance traveled
        # 4 Average bucket closure depth (average bucketZ at closure)
        #

        self.reportFrame14 =  pd.DataFrame(bucket_analyse,columns=['hours','AvgCcl/sec','buckets/h','Average bucket closure depth','ATBG'])
        self.average_time_cucle =  self.reportFrame14['AvgCcl/sec'].median()
        self.averagerozmah = self.reportFrame14['ATBG'].median()
        self.maxBucZ = self.dredging_df['BucketZ'].max()



        self.max_buccketZ  = self.dredging_df['BucketZ'].max()


        self.min_buccketZ = self.dredging_df['BucketZ'].min()

        # self.reportFrame14.plot.bar(x='hours',y='Number of buckets')
        # plt.show()



    def quantityAverage(self,arr):
        # arr = np.array(df['BucketZ'])
        max_peakind_index = signal.find_peaks_cwt(arr, np.arange(1, 90))

        max_peakind = arr[max_peakind_index]

        inv_data = -arr

        min_peakind_index = signal.find_peaks_cwt(inv_data, np.arange(1, 90))

        min_peakind_a = arr[min_peakind_index]

        b = np.diff(np.array(min_peakind_index))

        average_down_position = b[b < 150]

        ab_s = round(average_down_position.mean(), 2)

        quantity = len(min_peakind_a[min_peakind_a < 0])

        average_distantion = max(max_peakind)- min(min_peakind_a)

        max_bucket = max(min_peakind_a)
        if self.max_bucket < max_bucket:
            self.max_bucket = max_bucket

        return ab_s, quantity,average_down_position,average_distantion

    def closet_position(self):
        arr = np.array(self.dredging_df_out['BucketZ'])
        # max_peakind_index = signal.find_peaks_cwt(arr, np.arange(1, 90))

        # max_peakind = arr[max_peakind_index]

        inv_data = -arr

        min_peakind_index = signal.find_peaks_cwt(inv_data, np.arange(1, 90))

        # min_peakind_a = arr[min_peakind_index]

        # b = np.diff(np.array(min_peakind_index))

        # print(min_peakind_a)
        # average_down_position = b[b > -15]

        # ab_s = round(average_down_position.mean(), 2)
        #
        # quantity = len(min_peakind_a[min_peakind_a < 0])

        self.dredging_df_out.loc[:, "closed_bucket"] = np.nan
        self.dredging_df_out.loc[min_peakind_index,'closed_bucket'] = self.dredging_df_out.loc[min_peakind_index,"BucketZ"]
        self.dredging_df_out.loc[self.dredging_df_out["closed_bucket"] > -10, "closed_bucket"] = np.nan

        # print('BucketZ',list(self.dredging_df_out[:5000]['BucketZ']))
        # print('closed_bucket',list(self.dredging_df_out[:5000]['closed_bucket']))

    def Bucket_open_water_surface(self):
        pass


class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # self.canvas.setFocusPolicy(Qt.StrongFocus)



class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        font = QtGui.QFont()
        font.setItalic(True)
        font.setUnderline(True)
        Dialog.setFont(font)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(100, 80, 221, 131))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Save"))

class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        self.canvas = MplCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self)
        # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.toolbar)
        self.setLayout(self.vbl)




class Ui_MainWindow(ApplicationContext):

    def __init__(self):
        # matplotlib.use('Agg')#'QT5Agg')ьф
        # super(Ui_MainWindow, self).__init__()
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        # matplotlib.use('QT5Agg')



        self.dredging = Dredging()

        self.input_table_key = ['Time', 'BucketX', 'BucketY', 'BucketZ', 'BucketHdg', 'BoomAng',
                                'StickAng', 'BucketAng', 'Tide', 'BargeX', 'BargeY', 'BargeHdg',
                                'CraneDepth', 'CraneAngle', 'CraneLength', 'BoomLength', 'CabinX',
                                'CabinY', 'CabinZ', 'CabinHdg', 'DredgeZ', 'SurveyZ', 'DesignZ',
                                ]
        self.currentdir = None

        self.error_dialog = QtWidgets.QErrorMessage()
        self.error_msg = QtWidgets.QMessageBox()
        self.error_msg.setIcon(QtWidgets.QMessageBox.Critical)
        self.error_msg.setText("Error")
        self.error_msg.setWindowTitle("Error")
        self.old_start_position = None
        self.old_fin_position = None
        self.select_columns = ['BucketZ','BoomAng']


        # self.currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        # self.parentdir = os.path.dirname(self.currentdir)
        self.data_plot2 = None

        # self.data_queue = multiprocessing.Queue()


        # self.pool = multiprocessing.Pool()


        # self.dredging.dredging_df_out[:1000][['moveY', 'moveX', 'BoomAng', 'BucketZ']].plot()

    def plot1_data(self):
        self.data_plot1 = self.dredging.reportFrame14[
            ['hours', 'AvgCcl/sec', 'buckets/h', 'Average bucket closure depth', 'ATBG']]


        try:
            self.Graphic.canvas.ax.clear()
        except:
            pass
        self.Graphic.canvas.ax.bar(self.data_plot1['hours'], self.data_plot1['buckets/h'], color='#d62728',
                                       yerr=self.data_plot1['AvgCcl/sec'])

        self.Graphic.canvas.ax.set_title("Barchart")

        self.Graphic.canvas.draw()



    def plot2_data(self,start_position,fin_position):

        self.old_start_position = start_position
        self.old_fin_position = fin_position

        #maximum time

        self.data_plot2 = self.dredging.dredging_df.loc[self.old_start_position:self.old_fin_position]

        try:
            self.Graphic_2.canvas.ax.clear()
        except:
            pass

        self.Graphic_2.canvas.ax.plot(self.data_plot2[self.select_columns])

        self.Graphic_2.canvas.ax.set_title("Graphic2")

        self.Graphic_2.canvas.draw()


    def plot_data_new(self,plot_num=2):



        start_position = parse_time(self.timeEdit_from.text())  # .split()[1]
        fin_position = parse_time(self.timeEdit_to.text())  # .split()[1]




        if plot_num ==1:
            self.dredging.report_creat()
            self.plot1_data()

        elif plot_num ==2:

            if self.old_start_position == start_position and self.old_fin_position == fin_position and self.select_columns is None:
                return

            self.plot2_data(start_position,fin_position)

            # self.plot_data_new(plot_num=1)


    def plot_data(self,plot_num=3,x=None,y=None,start_position='00:00:00',fin_position='23:00:00'):

        start_position = str(parse_time(self.timeEdit_from.text()))#.split()[1]
        fin_position = str(parse_time(self.timeEdit_to.text()))#.split()[1]


        if self.old_start_position == start_position and self.old_fin_position == fin_position and self.select_columns is None:
            return

        elif self.select_columns and self.data_plot2 is not  None:
            try:
                self.Graphic_2.canvas.ax.clear()
                self.Graphic_2.canvas.ax.plot(self.data_plot2[self.select_columns])

                # self.Graphic.canvas.ax.plot(data[['BucketY','BargeY']])#data[['BucketZ','BoomAng']])
                self.Graphic_2.canvas.ax.set_title(y)

                self.Graphic_2.canvas.draw()
            except:
                self.error_msg.setInformativeText('Firs load file')
                self.error_msg.show()

            return

        else:


            self.old_start_position = start_position
            self.old_fin_position = fin_position
            self.data_plot1 = self.dredging.reportFrame14[
                ['hours', 'AvgCcl/sec', 'buckets/h', 'Average bucket closure depth', 'ATBG']]

            # print("time",self.old_start_position,self.old_fin_position)
            self.data_plot2  = self.dredging.dredging_df_out.loc[self.old_start_position:self.old_fin_position,:]

            if plot_num==1:

                self.Graphic.canvas.ax.clear()
                self.Graphic.canvas.ax.plot(self.data_plot1)

                self.Graphic.canvas.ax.set_title(y)

                self.Graphic.canvas.draw()

            elif plot_num == 2:
                self.Graphic_2.canvas.ax.clear()
                self.Graphic_2.canvas.ax.plot(self.data_plot2[self.select_columns])

                # self.Graphic.canvas.ax.plot(data[['BucketY','BargeY']])#data[['BucketZ','BoomAng']])
                self.Graphic_2.canvas.ax.set_title(y)

                self.Graphic_2.canvas.draw()

            else:

                self.Graphic.canvas.ax.clear()
                self.Graphic_2.canvas.ax.clear()
                #                       'hours', 'AvgCcl/sec', 'buckets/h', 'Average bucket closure depth', 'ATBG'
                self.Graphic.canvas.ax.bar(self.data_plot1['hours'],self.data_plot1['buckets/h'],color='#d62728',yerr=self.data_plot1['AvgCcl/sec'])

                self.Graphic_2.canvas.ax.plot(self.data_plot2[self.select_columns])


                self.Graphic.canvas.draw()
                self.Graphic_2.canvas.draw()





    def loadData(self):
        connection = sqlite3.connect('')#/Users/jbd/PycharmProjects/Dredging/dredging.db')
        query = "SELECT * FROM dredging1"
        result = connection.execute(query)


        for row_number,row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if row_number== 0:
                    print('row_number',data)

                self.tableWidget.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))

    def current_time(self):
        time = QtCore.QTime()
        curent_t = time.currentTime()
        return curent_t

    def load_data_pr(self):
        self.dredging.load_data(self.filename_now)
        if '/' in self.filename_now:

            self.filename_now = self.filename_now.split('/')[-1]
        elif '\\' in self.filename_now:
            self.filename_now = self.filename_now.split('\\')[-1]
        elif '\\' in self.filename_now:
            self.filename_now = self.filename_now.split('\\')[-1]

        io_lock = threading.RLock()
        executor = ThreadPoolExecutor(2)
        with io_lock:

            executor.submit(lambda: self.plot_data_new(plot_num=2))



    def load_data_(self):

        io_lock = threading.RLock()
        executor = ThreadPoolExecutor(3)
        with io_lock:

            self.load_data_pr()

            executor.submit(lambda: self.data_frame_to_ui())
            # future = self.pool.submit(lambda: self.load_data_pr())
            executor.submit(lambda: self.plot_data_new(plot_num=1))



    def get_data_csv(self):
        try:

            self.filename_now, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Open " + ' ' + " Data File", '.', "(*.csv)")
        except:
            self.error_msg.setInformativeText('Firs load file')
            self.error_msg.show()
            return
        io_lock = threading.RLock()
        executor = ThreadPoolExecutor(5)
        with io_lock:
            executor.submit(self.load_data_)




    def dataFrame_to_wiew(self):
        filename, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Open " + ' ' + " Data File", '.', "(*.csv)")

        with open(filename, 'r') as stream:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            for rowdata in csv.reader(stream):

                row = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row)
                self.tableWidget.setColumnCount(len(rowdata))

                for column, data in enumerate(rowdata):
                    item = QtWidgets.QTableWidgetItem(str(data))
                    self.tableWidget.setItem(row, column, item)

    def data_frame_todata_base(self):
        cnx = sqlite3.connect('dredging.db')

        # disk_engine = create_engine('sqlite:/Users/jbd/PycharmProjects/Dredging/dredging.db')
        # sql.write_frame(self.dredging.dredging_df, name='dredginginput21112018', con=cnx)
        self.dredging.dredging_df.to_sql('dredging2', cnx, if_exists='append')


    def data_frame_to_ui(self):


        # self.data_plot2 = self.dredging.dredging_df.loc[self.old_start_position:self.old_fin_position, :]

        # data_frame = self.dredging.dredging_df.loc[self.old_start_position:self.old_fin_position]


        self.tableWidget.insertRow(0)
        for column_number, data_ in enumerate(self.data_plot2.keys()):
            self.tableWidget.setItem(0, column_number, QtWidgets.QTableWidgetItem(str(data_)))

        for row_number, row_data in enumerate(self.data_plot2.values):
            self.tableWidget.insertRow(row_number+1)

            for column_number, data in enumerate(row_data):

                self.tableWidget.setItem(row_number+1, column_number, QtWidgets.QTableWidgetItem(str(data)))

    def pygraf_trying(self,plot_num=3,x=None,y=None,start_position='00:00:00',fin_position='23:00:00'):


        start_position = parse_time(self.timeEdit_from.text())
        fin_position = parse_time(self.timeEdit_to.text())
        data1  = self.dredging.dredging_df.loc[start_position:fin_position,:]
        data2 = self.dredging.dredging_df_out.loc[start_position:fin_position, :]
        if plot_num==1:

            self.Graphic.canvas.ax.clear()
            self.Graphic.canvas.ax.plot(data1[['BucketZ','BoomAng']])

            # self.Graphic.canvas.ax.plot(data[['BucketY','BargeY']])#data[['BucketZ','BoomAng']])
            self.Graphic.canvas.ax.set_title(y)


            self.Graphic.canvas.draw()



    def update_data_table_graphic(self):
        try:
            io_lock = threading.RLock()
            executor = ThreadPoolExecutor(5)
            with io_lock:
                executor.submit(self.plot_data_new(plot_num=2))
                self.data_frame_to_ui()


        except:
            self.error_msg.setInformativeText('Firs load file')
            self.error_msg.show()
            # self.error_dialog.showMessage('Firs load file')

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def item_tree_plots(self,it, col):
        arg = it.text(col)



    def printItemText(self):

        items = self.treeWidget_custom_plot.selectedItems()
        x = []
        for i in items:
            x.append(str(i.text(0)))
        if len(x) > 0:
            self.select_columns =  x
            self.plot_data()

    # def worker(self):
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(self.save())



    def save_new(self):


        try:
            self.currentdir = QtWidgets.QFileDialog.getExistingDirectory(
                None,
                "Select a folder" ,
                self.currentdir,
                QtWidgets.QFileDialog.ShowDirsOnly
            )

        except:
            pass


        # with ThreadPoolExecutor(10) as pool:
        # self.save()
        io_lock = threading.RLock()
        executor = ThreadPoolExecutor(2)
        with io_lock:
            executor.submit(self.save)

        # self.pool.apply(self.save)


        # self.p = Process(target=lambda: asyncio.get_event_loop().run_until_complete(self.save_new()))
        # # self.p = Process(target=self.worker())
        # self.p.daemon = True
        # self.p.start()

        # self.p.join()



    # @asyncio.coroutine
    def save(self):
        if self.currentdir is None:

            self.currentdir = expanduser("~")



        if self.currentdir is not None:

            self.os_sep = os.sep

            if '{0}report{1}'.format(self.os_sep,self.os_sep) in self.currentdir:
                self.currentdir = self.currentdir.replace('{0}report{1}'.format(self.os_sep,self.os_sep),self.os_sep)



            self.currentdir.replace('/',self.os_sep).replace('\\',self.os_sep)

            try:
                os.stat(os.path.join(self.currentdir,'report'))

            except:
                os.mkdir(os.path.join(self.currentdir,'report'))


            try:
                start_position = str(self.old_start_position).split()[1].replace(':','_')
                fin_position = str(self.old_fin_position).split()[1].replace(':','_')
            except:
                start_position = "00_00_00"
                fin_position = "04_00_00"

            self.data_plot2.to_csv(os.path.join(
                self.currentdir,"report","{0}_{1}_{2}.csv".format(self.filename_now.replace(".csv", ""),
                                                                  start_position,
                                                                  fin_position)))

            plot = self.data_plot2[self.select_columns].plot()
            fig = plot.get_figure()
            fig.set_size_inches(45.5, 10.5)

            fig.savefig(os.path.join(self.currentdir,"report","{0}_{1}_{2}_{3}.png".format(
                                                                                        self.filename_now.replace(".csv",""),
                                                                                       "_".join(self.select_columns),
                                                                                       start_position,
                                                                                       fin_position
                                                                                      )
                                     ))


            # self.data1.to_csv(os.path.join(self.currentdir + "/reports/", "report2.csv"))





    def tableWidget_init(self):

        self.tableWidget.insertRow(0)
        for column_number, data in enumerate(self.input_table_key):
            # self.tableWidget.setIte
            self.tableWidget.setItem(0, column_number, QtWidgets.QTableWidgetItem(str(data)))


    def dialog(self):

        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Dredging Analytic")
        MainWindow.resize(1581, 1005)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        self.tableWidget = QtWidgets.QTableWidget(self.centralWidget)
        self.tableWidget.setGeometry(QtCore.QRect(40, 700, 1201, 171))
        self.tableWidget.setRowCount(99)
        self.tableWidget.setColumnCount(50)
        self.tableWidget.setObjectName("tableWidget")


        l1 = QtWidgets.QTreeWidgetItem(["Plot1"])
        l2 = QtWidgets.QTreeWidgetItem(["Plot2"])

        for i in self.input_table_key:
            l1_child = QtWidgets.QTreeWidgetItem([i])
            l1.addChild(l1_child)

        for j in range(2):
            l2_child = QtWidgets.QTreeWidgetItem(["Child AA" + str(j), "Child BB" + str(j), "Child CC" + str(j)])
            l2.addChild(l2_child)

        self.treeWidget_custom_plot = QtWidgets.QTreeWidget(self.centralWidget)
        self.treeWidget_custom_plot.setGeometry(QtCore.QRect(1370, 20, 211, 211))
        self.treeWidget_custom_plot.setObjectName("treeWidget_custom_plot")
        self.treeWidget_custom_plot.headerItem().setText(0, "1")
        self.treeWidget_custom_plot.setHeaderLabels(["Plot name"])
        self.treeWidget_custom_plot.addTopLevelItem(l1)
        # self.treeWidget_custom_plot.itemDoubleClicked.connect(self.item_tree_plots)
        self.treeWidget_custom_plot.itemClicked.connect(self.printItemText)
        self.treeWidget_custom_plot.addTopLevelItem(l2)
        self.treeWidget_custom_plot.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.Graphic = MplWidget(self.centralWidget)
        self.Graphic.setGeometry(QtCore.QRect(30, 10, 1331, 381))
        self.Graphic.setObjectName("Graphic")

        self.Graphic_2 = MplWidget(self.centralWidget)
        self.Graphic_2.setGeometry(QtCore.QRect(30, 390, 1331, 261))
        self.Graphic_2.setObjectName("Graphic_2")

        self.widget = QtWidgets.QWidget(self.centralWidget)
        self.widget.setGeometry(QtCore.QRect(1100, 640, 311, 52))
        self.widget.setObjectName("widget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.load_graphic = QtWidgets.QPushButton(self.widget)
        self.load_graphic.setObjectName("load_graphic")
        self.load_graphic.clicked.connect(
            lambda: self.update_data_table_graphic())
        self.horizontalLayout.addWidget(self.load_graphic)

        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setToolTip('This is a <b>QPushButton</b> widget')
        self.pushButton_2.clicked.connect(
            lambda: self.dredging.visualize(x_='BucketZ'))
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2.setToolTip('This is a <b>set </b> widget')
        self.pushButton.clicked.connect(
            lambda: self.dredging.visualize(x_='BucketZ'))
        self.horizontalLayout.addWidget(self.pushButton)

        self.widget1 = QtWidgets.QWidget(self.centralWidget)
        self.widget1.setGeometry(QtCore.QRect(1250, 690, 185, 126))
        self.widget1.setObjectName("widget1")

        self.gridLayout = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")

        self.timeEdit_from = QtWidgets.QTimeEdit(self.widget1)
        self.timeEdit_from.setObjectName("timeEdit_from")
        self.gridLayout.addWidget(self.timeEdit_from, 0, 1, 1, 1)

        self.dateEdit = QtWidgets.QDateEdit(self.widget1)
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout.addWidget(self.dateEdit, 1, 0, 1, 1)

        self.timeEdit_to = QtWidgets.QTimeEdit(self.widget1)
        self.timeEdit_to.setObjectName("timeEdit_to")
        self.timeEdit_to.setTime(QtCore.QTime.fromString("04:00"))
        self.gridLayout.addWidget(self.timeEdit_to, 2, 1, 1, 1)

        self.load_file_butom = QtWidgets.QPushButton(self.widget1)
        self.load_file_butom.setObjectName("load_file_butom")
        self.load_file_butom.clicked.connect(lambda: self.get_data_csv())
        self.gridLayout.addWidget(self.load_file_butom, 3, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")

        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")

        MainWindow.setStatusBar(self.statusBar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1581, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menuBar)
        self.menuEdit.setObjectName("menuEdit")

        MainWindow.setMenuBar(self.menuBar)
        self.actionOpen_file = QtWidgets.QAction(MainWindow)
        self.actionOpen_file.setObjectName("actionOpen_file")

        self.actionOpen_file.setShortcut("Ctrl+O")
        self.actionOpen_file.triggered.connect(lambda : self.get_data_csv())


        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionClose.setShortcut("Ctrl+Q")
        self.actionClose.triggered.connect(lambda: QtCore.QCoreApplication.exit(0))

        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")

        self.actionRedo = QtWidgets.QAction(MainWindow)
        self.actionRedo.setObjectName("actionRedo")

        self.actionSave_to = QtWidgets.QAction(MainWindow)
        self.actionSave_to.setObjectName("actionSave_to")

        self.actionSave = QtWidgets.QAction(MainWindow)

        self.actionSave.setObjectName("actionSave")
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave.triggered.connect(lambda: self.save_new())

        self.actionReport = QtWidgets.QAction(MainWindow)
        self.actionReport.setObjectName("actionSave")
        self.actionReport.setShortcut("Ctrl+R")
        self.actionReport.triggered.connect(lambda: self.save_new())


        self.menuFile.addAction(self.actionOpen_file)

        self.menuFile.addAction(self.actionClose)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionSave_to)
        self.menuEdit.addAction(self.actionSave)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Dredging Analytic", "Dredging Analytic"))
        self.load_graphic.setText(_translate("Dredging Analytic", "select graphic"))
        self.pushButton_2.setText(_translate("Dredging Analytic", "set"))
        self.pushButton.setText(_translate("Dredging Analytic", "clean"))
        self.load_file_butom.setText(_translate("Dredging Analytic", "Load file"))
        self.toolBar.setWindowTitle(_translate("Dredging Analytic", "toolBar"))
        self.menuFile.setTitle(_translate("Dredging Analytic", "File"))
        self.menuEdit.setTitle(_translate("Dredging Analytic", "Edit"))
        self.actionOpen_file.setText(_translate("Dredging Analytic", "Open file"))
        self.actionClose.setText(_translate("Dredging Analytic", "Close"))
        self.actionUndo.setText(_translate("Dredging Analytic", "Undo"))
        self.actionRedo.setText(_translate("Dredging Analytic", "Redo"))
        self.actionSave_to.setText(_translate("Dredging Analytic", "Save to"))
        self.actionSave.setText(_translate("Dredging Analytic", "Save"))

def main():
    import sys
    import os

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # MainWindow.setStyleSheet("background-color: black;")

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()


    sys.exit(app.exec_())

if __name__ == "__main__":
    main()