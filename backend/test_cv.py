import argparse
from utils.detect.detect import get_detection_result


parser = argparse.ArgumentParser()

parser.add_argument('--model_type', required=True, help='mediapipe or facenet')
parser.add_argument('--filepath', required=True, help='path to videofile')
args = parser.parse_args()

model_type = args.model_type
filepath = args.filepath

get_detection_result(model_type, filepath, debug=True)
