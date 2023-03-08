import time

import qrcode
from PIL import Image
# Data to encode
data = "GeeksforGeeks"

img_bg = Image.open('qrw.png')
img_bg = img_bg.convert('RGB')

# Creating an instance of QRCode class
print((t1:= time.time()))
pos = (20, 30)
pos2 = (80, 60)

qr = qrcode.QRCode(version=1,
                       box_size=30,
                       border=0)

for i in range(100):
    # Adding data to the instance 'qr'
    qr.clear()
    qr.add_data(data)
    qr.make(fit=True)
    img_qr = qr.make_image(back_color='white')
    img_bg.paste(img_qr, pos)
    img_bg.paste(img_qr, pos2)
    img_bg.save(f'info/{i}.JPEG')


print((t21:= time.time()))
print(t21-t1)
