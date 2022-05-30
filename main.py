from typing import Dict, Any

from flask import Flask, Blueprint, make_response
from flask_restx import Resource, Api

from werkzeug.datastructures import FileStorage
from ocr import OCR

flask = Flask("MultiNLU")
api = Api(version="0.1", title="Diagram OCR API", default_label="Fallback API", default="Fallback")

ns = api.namespace("ocr", "ocr namespace")

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

ocr = OCR()

@ns.route("/")
class OCREndpoint(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @api.expect(upload_parser)
    @api.response(200, "if recognition was successful")
    def post(self) -> Dict[str, Any]:
        args = upload_parser.parse_args()
        uploaded_file : FileStorage = args['file']  # This is FileStorage instance
        data = uploaded_file.read()
        result = ocr.interprete(data)
        print(result)
        return result

    @api.response(200, f"Hello from Sketch Recognition {api.version}")
    @api.produces(['text/plain'])
    def get(self):
        response = make_response(f"Hello from OCR {api.version}")
        response.headers.set("Content-Type", "text/plain")
        return response


if __name__ == '__main__':
    blueprint = Blueprint('api', __name__)

    api.init_app(blueprint)
    api.add_namespace(ns)

    flask.register_blueprint(blueprint)
    # Debug
    flask.run(host="0.0.0.0", port=5005, debug=False)

    # Production
    # from waitress import serve
    # serve(flask, host="0.0.0.0", port=5005)