import cv2
import tensorflow
import sys

print("cv2 version:", cv2.__version__)
print("tf version:", tensorflow.__version__)
print("Python version:", sys.version, sys.version_info)

cap = cv2.VideoCapture(0)
