import cv2

videoCapture = cv2.VideoCapture('output.avi')
fps = videoCapture.get(cv2.cv.CV_CAP_PROP_FPS)
print fps

size = (int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
        int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
print size

videoWriter = cv2.VideoWriter(
    'opencvoutput.avi', cv2.cv.CV_FOURCC('P','I','M','1'), fps, size) #formato MPEG-1

success, frame = videoCapture.read()


while sucess: #loop ate nao ter mais frames
    videoWriter.write(frame)
    sucess, frame = videoCapture.read()



