import cv2
import time
import os
import subprocess
from picamera2 import Picamera2
import numpy as np


save_dir = os.path.join(
    os.path.expanduser("~"),
    "captures"
)
os.makedirs(save_dir, exist_ok=True)


face_cascade = cv2.CascadeClassifier(
    "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
)

picam2 = Picamera2()
picam2.configure(
    picam2.create_preview_configuration(
        main={
            "size": (640, 480),
            "format": "BGR888"
        }
    )
)
picam2.start()


prev_gray = None
last_saved = 0
save_cooldown = 5 # 5 second wait
motion_score = 0


while True:
    frame = picam2.capture_array()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    motion_detected = False

    if prev_gray is not None:
        diff = cv2.absdiff(prev_gray, gray)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        motion_score = np.sum(thresh) / 255
    
        if motion_score > 2000:
            motion_detected = True

    prev_gray = gray

    if not motion_detected:
        time.sleep(0.05)
        continue

    faces = face_cascade.detectMultiScale(gray, 1.2, 5)

    now = time.time()

    if len(faces) > 0 and (now - last_saved > save_cooldown):

        timestamp = time.strftime('%Y%m%d_%H%M%S')

        filename = os.path.join(
            save_dir,
            f"detection_{timestamp}.jpg"
        )

        cv2.imwrite(filename, frame)
        print(f"\n[SAVED] {filename}")
        last_saved = now
        result = subprocess.run(
            ["php", "/home/username123/sendAlert.php", filename],
            capture_output=True,
            text=True
        )

        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

    print(f"\rMotion: {motion_score:.0f} | Faces: {len(faces)}    ", end="", flush=True)
    time.sleep(0.05)


