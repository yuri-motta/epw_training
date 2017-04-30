import os

"""no servidor video streaming deve-se colocar o ip do client"""

os.system('ffmpeg -r 30 -i /dev/video0 -f h264 -pix_fmt yuv422p -an -preset ultrafast -f mpegts udp://192.168.1.144:4445')
