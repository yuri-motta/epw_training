import cv2
import numpy

## le as imagens e salva como BGR (mesma coisa que RGB mas ao contrario) obs: converte para bgr mesmo uma imagem em escalas de cinza
image = cv2.imread('Fig0646(a)(lenna_original_RGB).tif')

## salva a imagem
cv2.imwrite('Fig0646(a)(lenna_original_RGB).jpg',image)

## salva a imagem em tons de cinza
grayImage = cv2.imread('Fig0646(a)(lenna_original_RGB).tif', cv2.CV_LOAD_IMAGE_GRAYSCALE)
cv2.imwrite('Fig0646(a)(lenna_grayscale).tif',grayImage)


## le a imagem em uma array unidimensional
bytearray = bytearray(grayImage)
#print bytearray
