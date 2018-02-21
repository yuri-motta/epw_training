#!/bin/bash

echo "Starting system's preparation"
sudo apt-get update
echo "Updgrading Ubuntu Version"
sudo apt-get upgrade
echo "installing ffmpeg library"
sudo apt-get install ffmpeg
echo "installing python tkinter library"
sudo apt-get install python-tk
echo "installing python pip"
sudo apt-get install python-pip
echo "installing pillow library"
sudo pip install pillow




