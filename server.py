#!/usr/bin/env python3

import cv2
import socket
import struct
import pickle

HOST = '127.0.0.1'
PORT = 65432


if __name__ == "__main__":
    data = b""
    payload_size = struct.calcsize("Q")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                while len(data) < payload_size:
                    data += conn.recv(4*1024)
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]
                while len(data) < msg_size:
                    data += conn.recv(4*1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                    
                frame = pickle.loads(frame_data)
                if frame is not None:
                    cv2.imshow("Received Frame", frame)


                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            conn.close()
            cv2.destroyAllWindows()