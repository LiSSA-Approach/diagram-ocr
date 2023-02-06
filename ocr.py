from typing import List

import numpy as np
import cv2
import easyocr


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

        normalized = cv2.normalize(image, None, alpha=0, beta=1.2, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        normalized = np.clip(normalized, 0, 1)
        image = (255 * normalized).astype(np.uint8)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # image = cv2.blur(image, (3, 3))
        # image = cv2.Canny(image, 100, 200)

        # cv2.imwrite(f"./image{self._ctr}.png", image)
        self._ctr += 1

        reader = easyocr.Reader(['en'])
        result = reader.readtext(image)

        result_data = []
        for (bbox, text, confidence) in result:
            (tl, tr, _, bl) = bbox
            tl = (int(tl[0]), int(tl[1]))
            tr = (int(tr[0]), int(tr[1]))
            bl = (int(bl[0]), int(bl[1]))
            (x, y, w, h) = (tl[0], tl[1], tr[0] - tl[0], bl[1] - tl[1])
            entry = {
                "x": x + x1,
                "y": y + y1,
                "w": w,
                "h": h,
                "text": text,
                "confidence": float(confidence)
            }
            if len(entry["text"].strip()) == 0:
                continue

            result_data.append(entry)
        return result_data
