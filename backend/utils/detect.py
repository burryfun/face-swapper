import cv2
import json
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


def get_detection_result(video_path):
    output = {'data': []}

    cap = cv2.VideoCapture(video_path)
    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
        while cap.isOpened():

            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                break

            image_width, image_heigth = image.shape[1], image.shape[0]

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_detection.process(image)

            # Draw the face detection annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            frame_data = None
            if results.detections:
                for detection in results.detections:
                    face_id = detection.label_id[0]
                    bbox = detection.location_data.relative_bounding_box
                    xmin, ymin, width, height = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                    xmax, ymax = xmin + width, ymin + height
                    xmin, ymin, xmax, ymax = xmin*image_width, ymin*image_heigth, xmax*image_width, ymax*image_heigth
                    xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)

                    frame_data = [xmin, ymin, xmax, ymax, face_id]

            output['data'].append(frame_data)
            
    cap.release()

    output = json.dumps(output)

    return output
