#!/usr/bin/env python3

import cv2
import socket
import pickle
import struct

HOST = '127.0.0.1'
PORT = 65432

def get_cam(width, height):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return cap

def get_frame(cap):
    ret, frame = cap.read()
    if ret:
        print("INFO: read frame successfully!")
        return frame
    else:
        print("ERROR: failed read frame!")
        return None


if __name__ == "__main__":
    # User can specify the video list here.
    #show_cameras([2, 6, 10, 14])
 
    # Or search all available video devices automatically.
    cap = get_cam(640,360)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            frame = get_frame(cap)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            # print(frame_bytes)
            s.sendall(message)