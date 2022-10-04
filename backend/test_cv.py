import argparse
from utils.detect.detect import Detectors, get_detection_result


parser = argparse.ArgumentParser()

parser.add_argument('--model_type', type=Detectors.argparse,
                    choices=list(Detectors), required=True, help='choose model for detection')
parser.add_argument('--filepath', required=True, help='path to videofile')
parser.add_argument('--device', default=None, help='cpu or cuda')
args = parser.parse_args()

model_type = args.model_type
filepath = args.filepath
device = args.device

get_detection_result(model_type, filepath, debug=True, device=device)
