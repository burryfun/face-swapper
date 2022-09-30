from enum import Enum
import cv2
import json
from utils.detect.mediapipe_detector import MediapipeDetector
from utils.detect.facenet_detector import FaceNetDetector

FONT = cv2.FONT_HERSHEY_SIMPLEX
class Detectors(Enum):
    MEDIAPIPE = MediapipeDetector
    FACENET = FaceNetDetector

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return str(self)
        
    @staticmethod
    def argparse(s):
        try:
            return Detectors[s.upper()]
        except KeyError:
            return s

def get_detection_result(detector_name: Detectors, video_path: str, debug: bool = False) -> str:
    output = {'data': []}

    # Type checking
    if not isinstance(detector_name, Detectors):
        raise TypeError('detector must be an instance of Detectors Enum')

    detector = detector_name.value()

    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():

        success, image = cap.read()
        if not success:
            print("END")
            break

        frame_data = detector.detect_and_track(image)

        if debug:
            if frame_data is not None:
                for face_data in frame_data:
                    xmin, ymin, xmax, ymax, face_id = face_data
                    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
                    cv2.putText(image, str(face_id), (xmin, ymin), FONT, 1, (255, 0, 0), 2, cv2.LINE_AA)

        output['data'].append(frame_data)

        if debug:
            cv2.imshow('image', image)
            cv2.waitKey(1)

    cap.release()

    output = json.dumps(output)

    return output


