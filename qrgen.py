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
        img_bg.save(f'QrPay{hash__}.png')


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
        img_bg.save(f'QrInfo{hash__}.png')

# for i in range(40):
#
#
#     createQRINFO()
#     createQRPAY()
#     print(i)

# createQRINFO(20)
# createQRINFO(20)
# createQRPAY(20)
# createQRPAY(20)
thread1 = threading.Thread(target=createQRINFO,args=(20,))
thread2 = threading.Thread(target=createQRINFO,args=(20,))
thread3 = threading.Thread(target=createQRPAY,args=(20,))
thread4 = threading.Thread(target=createQRPAY,args=(20,))

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()


# createQRPAY()
# hash_ = createhach()
# print(hash_)
# url = pyqrcode.create(f'https://qpayinc.herokuapp.com/q/{hash_}/')
# url.png('code.png', scale=6)
# # url.png('uca-url.png', scale=8)