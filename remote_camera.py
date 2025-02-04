import cv2
from flask import Flask
import threading
import time
import os
import sys
import pyautogui
is_recording = False
def click():
    while True:
        pyautogui.click()
        time.sleep(10)
    
def record_video(output_path, duration=10):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot open camera.")
        return

    frame_width = 640
    frame_height = 480
    print(f"Camera resolution: {frame_width}x{frame_height}")
    fourcc = cv2.VideoWriter_fourcc(*'XVID') 
    fps =30 
    print(f"fps:{fps}")
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    print(f"Recording started. Duration: {duration} seconds.")

    start_time = cv2.getTickCount()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break
        out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if (cv2.getTickCount() - start_time) / cv2.getTickFrequency() >= duration:
            print("Recording completed.")
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def keep_recording(folder,duration):
    while is_recording:
        record_video(f'{folder}/{str(int(time.time()))}.avi', duration=duration)



app = Flask(__name__)
@app.route('/record/start')
def record():
   
    global is_recording
    if(is_recording):
        return "Already recording!"
    is_recording = True
    timestamp = str(int(time.time()))
    try:
        os.mkdir(f'scripts/{timestamp}')
    except FileExistsError:
        pass

    threading.Thread(target=keep_recording, args=[f'scripts/{timestamp}', 300]).start()
    threading.Thread(target=click).start()
    return 'Recording started. Please wait...'  

@app.route('/record/stop')
def stop_record():
    global is_recording
    is_recording = False
    os._exit(0)
    return 'Recording stopped.'
app.run(host='0.0.0.0', port=5000)
  



