import cv2
import os

class VideoProcessing:
    def __init__(self, filename: str):
        self.video = cv2.VideoCapture(filename)

    def get_frame(self, sec: float):
        self.video.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        return self.video.read()

    def to_images(self, to=""):
        sec: float = 0.0
        frame_rate: float = 0.5
        count: int = 0
        while True:
            has_frame, image = self.get_frame(sec)
            if not has_frame:
                break
            cv2.imwrite(f"{to}/image-{sec}.jpg", image)
            count = count + 1
            sec = sec + frame_rate
            sec = round(sec, 2)

    def meshroom(self, input="", output=""):
        return os.system(f"./meshroom/meshroom_photogrammetry --input {input} --output {output}")
