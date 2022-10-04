import cv2
import torch
from facenet_pytorch import MTCNN
from utils.detect.sort import Sort


class FaceNetDetector(object):

    def __init__(self, device=None):
        if device is None:
            device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

        print(f'Using device: {device}')
        self.detector = MTCNN(image_size=160, keep_all=True, margin=0, min_face_size=20,
                              thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
                              device=device)
        self.tracker = Sort(max_age=8)

    def detect_and_track(self, image):
        image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes, _ = self.detector.detect(image)

        if boxes is not None:
            boxes = self.tracker.update(boxes)

            frame_data = []
            for bbox in boxes:
                #print(bbox)
                xmin, ymin, xmax, ymax, face_id = bbox
                xmin, ymin, xmax, ymax, face_id = int(xmin), int(ymin), int(xmax), int(ymax), int(face_id)

                frame_data.append([xmin, ymin, xmax, ymax, face_id])
        else:
            boxes = self.tracker.update()
            frame_data = None

        return frame_data
