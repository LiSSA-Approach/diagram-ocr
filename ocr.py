import numpy as np
import cv2
import pytesseract

class OCR:
    def __init__(self):
        pass

    def interprete(self, data: bytes):  # -> Union[str, dict]:
        try:
            npdata = np.fromstring(data, np.uint8)
            image = cv2.imdecode(npdata, cv2.IMREAD_COLOR)
        except Exception as error:
            return f"Could not predict: {error}"

        d = pytesseract.image_to_data(image, lang="eng", output_type=pytesseract.Output.DICT)
        n_boxes = len(d['level'])
        result_data = []
        for i in range(n_boxes):
            if d['conf'][i] == '-1':
                continue
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            entry = {
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "text": d['text'][i]
            }
            if len(entry["text"].strip()) == 0:
                continue

            result_data.append(entry)
        return result_data
