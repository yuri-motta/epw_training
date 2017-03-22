import cv2
import numpy

## le a imagem bgr e converte para grayscale
grayImage = cv2.imread('Fig0646(a)(lenna_original_RGB).jpg', cv2.CV_LOAD_IMAGE_GRAYSCALE)


grayImageArray = numpy.array(grayImage)

print grayImageArray