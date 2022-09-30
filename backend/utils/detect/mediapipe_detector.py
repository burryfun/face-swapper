import cv2
import json
import mediapipe as mp


mp_face_detection = mp.solutions.face_detection

class MediapipeDetector(object):

    def __init__(self, model_selection=1):
        self.detector = mp_face_detection.FaceDetection(model_selection=model_selection,
                                                        min_detection_confidence=0.5)

    def detect_and_track(self, image):
        image_width, image_heigth = image.shape[1], image.shape[0]
        image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.detector.process(image_RGB)

        if results.detections:
            frame_data = []
            for detection in results.detections:
                face_id = detection.label_id[0]
                bbox = detection.location_data.relative_bounding_box
                xmin, ymin, width, height = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                xmax, ymax = xmin + width, ymin + height
                xmin, ymin, xmax, ymax = xmin*image_width, ymin*image_heigth, xmax*image_width, ymax*image_heigth
                xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)

                frame_data.append([xmin, ymin, xmax, ymax, face_id])
        else:
            frame_data = None

        return frame_data
