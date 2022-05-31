from typing import List

import numpy as np
import cv2
import pytesseract


class OCR:
    def __init__(self):
        self._ctr = 0

    def interpret(self, data: bytes, regions: List[List[int]]):  # -> Union[str, dict]:
        try:
            npdata = np.fromstring(data, np.uint8)
            image = cv2.imdecode(npdata, cv2.IMREAD_COLOR)
            height, width, channels = image.shape
        except Exception as error:
            return f"Could not predict: {error}"

        if len(regions) == 0:
            regions = [[0, 0, width - 1, height - 1]]

        result_data = []
        for region in regions:
            found_data = self._process_region(image.copy(), region, width, height)
            result_data += found_data
        return result_data

    def _process_region(self, original_image, region, original_width, original_height):

        x1, y1, x2, y2 = region[0], region[1], region[2], region[3]
        # Ensure correct dimensions
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(x2, original_width - 2)
        y2 = min(y2, original_height - 2)

        image = original_image[y1:y2, x1:x2]
        cv2.imwrite(f"./image{self._ctr}.png", image)
        self._ctr += 1
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
