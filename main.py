from typing import List, Union

from flask import Flask, Blueprint, make_response, abort
from flask_restx import Resource, Api
from werkzeug.datastructures import FileStorage

from ocr import OCR

flask = Flask("DiagramOCR")
api = Api(version="0.1", title="Diagram OCR API", default_label="Fallback API", default="Fallback")

ns = api.namespace("ocr", "ocr namespace")

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
upload_parser.add_argument('regions', location='args', type=str, help="(x1,y1,x2,y2) x N", required=False)
ocr = OCR()


@ns.route("/")
class OCREndpoint(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @api.expect(upload_parser)
    @api.response(200, "if recognition was successful")
    @api.response(400, "if the parameters are not good")
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file: FileStorage = args['file']  # This is FileStorage instance
        regions: Union[str, List[List[int]]] = args['regions']
        if not regions:
            regions = []
        else:
            ints = [int(value.strip()) for value in regions.split(",")]
            if len(ints) % 4 != 0:
                abort(400, "You cannot provided regions % 4 != 0")
            regions = [ints[i:i + 4] for i in range(0, len(ints), 4)]

        data = uploaded_file.read()
        result = ocr.interpret(data, regions)
        # print(result)
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
    # flask.run(host="0.0.0.0", port=5005, debug=False)

    # Production
    from waitress import serve
    serve(flask, host="0.0.0.0", port=5005)
