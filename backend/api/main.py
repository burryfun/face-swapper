import os
import sys
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from os import path
import werkzeug

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from utils.detect import get_detection_result

UPLOAD_FOLDER = os.path.join(path.dirname(path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

class upload(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')

    def post(self):
        request_data = self.parser.parse_args()
        print(f'\nINFO: Data from request:\n\t{request_data}\n')

        file = request_data['file']
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        print(f'INFO: {filename} saved to {UPLOAD_FOLDER}\n')

        detection_result = get_detection_result(filepath)
        response = app.response_class(
            response=detection_result,
            status=200,
            mimetype='application/json'
        )
        return response

api.add_resource(upload, "/upload")

app.run()

