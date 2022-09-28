import sys
from flask import Flask
from flask_restful import Api, Resource, reqparse
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from utils.detect import get_detection_result

app = Flask(__name__)
api = Api(app)

class Detection(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('filepath', type=str, required=True)

    def post(self):
        request_data = self.parser.parse_args()
        print(f'\nData from request:\n\t{request_data}\n')

        filepath = request_data['filepath']

        detection_result = get_detection_result(filepath)
        response = app.response_class(
            response=detection_result,
            status=200,
            mimetype='application/json'
        )
        return response

api.add_resource(Detection, "/")

app.run(host="localhost", port=5000)

