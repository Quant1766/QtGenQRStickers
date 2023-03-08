import cv2
import numpy as np

qr_temp_path = 'qrtemp.png'
img = cv2.imread(qr_temp_path)

black_pixels = np.where(
    (img[:, :, 0] <= 30) &
    (img[:, :, 1] <= 30) &
    (img[:, :, 2] <= 30)
)

# set those pixels to white
img2 = img.copy()
noblack_pixels = np.where(
    (img2[:, :, 0] >= 30) &
    (img2[:, :, 1] >= 30) &
    (img2[:, :, 2] >= 30)
)
img2[noblack_pixels] = [255, 255, 255]
img2[black_pixels] = [0, 0, 255]

cv2.imshow("img",img)
cv2.imshow("img2",img2)

cv2.waitKey(0)

# closing all open windows
cv2.destroyAllWindows()