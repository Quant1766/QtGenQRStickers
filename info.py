from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QMessageBox, QVBoxLayout
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

import requests
from requests.auth import HTTPBasicAuth


import json

import qrcode
from PIL import Image
import threading
import secrets, png



def createhach():
    generated_key = secrets.token_urlsafe(6).replace("-", "_").replace("+", "_").replace(".", "_")
    return generated_key


def createQRPAY(n_):
    for i in range(1, n_):
        img_bg = Image.open('qpayPay.png')

        qr = qrcode.QRCode(box_size=73)
        hash__ = createhach()
        qr.add_data(f'https://qpayinc.herokuapp.com/q/{hash__}/')
        qr.make()
        img_qr = qr.make_image()

        pos = (img_bg.size[0] - img_qr.size[0] - 150, img_bg.size[1] - img_qr.size[1] - 1050)

        img_bg.paste(img_qr, pos)
        img_bg.save(f'Pay/QrPay{hash__}.png')


def createQRINFO(n_):
    for i in range(1,n_):
        img_bg = Image.open('qpayInfo.png')
        hash__ = createhach()
        qr = qrcode.QRCode(box_size=73)
        qr.add_data(f'https://qpayinc.herokuapp.com/q/{hash__}/')
        qr.make()
        img_qr = qr.make_image()

        pos = (img_bg.size[0] - img_qr.size[0] - 150, img_bg.size[1] - img_qr.size[1] - 1050)

        img_bg.paste(img_qr, pos)
        img_bg.save(f'info/QrInfo{hash__}.png')


class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Insert Data"
        self.top = 100
        self.left = 100
        self.width = 300
        self.height = 100


        self.error_dialog = QtWidgets.QErrorMessage()
        self.error_msg = QtWidgets.QMessageBox()

        self.currentdir = None


        self.InitWindow()


    def createQrs(self):
        thread1 = threading.Thread(target=createQRINFO, args=(20,))
        thread2 = threading.Thread(target=createQRINFO, args=(20,))
        thread3 = threading.Thread(target=createQRPAY, args=(20,))
        thread4 = threading.Thread(target=createQRPAY, args=(20,))

        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()

    # def setFile(self):
    def saveCurrentDir(self):
        self.currentdir = QtWidgets.QFileDialog.getExistingDirectory(
            None,
            "Select a folder",
            self.currentdir,
            QtWidgets.QFileDialog.ShowDirsOnly
        )

    def set_BBSDatas(self):
        self.filesname_now, _filter = QtWidgets.QFileDialog.getOpenFileNames(None,
                            "Open " + ' ' + " Data File",
                            '.', "(*.json)")

        resp_datas = []

        for file_name in self.filesname_now:
            res = requests.get("https://qpayinc.app/api/businessbuysale/load/companys/",
                               auth=HTTPBasicAuth("quant", "torrent641"))

            headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

            res = requests.post(res.url,
                                auth=HTTPBasicAuth("quant", "torrent641"),
                                data=open(file_name, 'rb').read(),
                                headers=headers)
            resp_datas.append(f"{file_name} {res.json()['Status']}")

        self.error_msg.setInformativeText("\n".join(resp_datas))
        self.error_msg.show()

    def set_BBSData(self):
        res = requests.get("https://qpayinc.app/api/businessbuysale/load/companys/",auth=HTTPBasicAuth("quant","torrent641"))
        self.filename_now, _filter = QtWidgets.QFileDialog.\
            getOpenFileName(None,
                            "Open " + ' ' + " Data File",
                            '.', "(*.json)")

        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

        res = requests.post(res.url,
                            auth=HTTPBasicAuth("quant","torrent641"),
                            data=open(self.filename_now, 'rb').read(),
                            headers=headers)

        self.error_msg.setInformativeText(res.json()['Status'])
        self.error_msg.show()




    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        vbox = QVBoxLayout()

        # self.name = QLineEdit(self)
        # self.name.setPlaceholderText('Please Enter Your Name')
        # # self.name.setStyleSheet('background:yellow')
        # self.name.setFont(QtGui.QFont("Sanserif", 10))
        #
        # vbox.addWidget(self.name)

        # self.email = QLineEdit(self)
        # self.email.setPlaceholderText('Please Enter Your Email')
        # self.email.setFont(QtGui.QFont("Sanserif", 10))
        # self.email.setStyleSheet('background:yellow')

        # vbox.addWidget(self.email)

        self.actionOpen_file = QtWidgets.QAction(self)
        self.actionOpen_file.setObjectName("actionOpen_file")
        self.actionOpen_file.setShortcut("Ctrl+O")



        self.button = QPushButton("Insert Data", self)
        # self.button.setStyleSheet('background:green')

        self.button.setFont(QtGui.QFont("Sanserif", 10))
        vbox.addWidget(self.button)
        self.button.clicked.connect(self.set_BBSDatas)

        self.button = QPushButton("Qreate QR", self)
        # self.button.setStyleSheet('background:green')

        self.button.setFont(QtGui.QFont("Sanserif", 10))
        vbox.addWidget(self.button)
        self.button.clicked.connect(self.createQrs)

        self.setLayout(vbox)

        self.show()





def main():
    import sys
    import os
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())



if __name__ == "__main__":
    main()

