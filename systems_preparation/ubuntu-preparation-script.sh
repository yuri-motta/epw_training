#!/bin/bash

echo "Starting system's preparation"
sudo apt-get update
echo "installing ffmpeg library"
sudo apt-get install ffmpeg
echo "installing python tkinter library"
sudo apt-get install python-tk
echo "installing pillow library"
sudo pip install pillow

echo "Your system is ready! Thank you"


