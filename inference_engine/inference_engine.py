import logging
import cv2
import numpy as np


class InferenceEngine:

    @staticmethod
    def to_numpy(img):
        logging.debug("converting image to numpy array")

    @staticmethod
    def make_inference(image_bytes, name="default_name"):
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
        logging.info("making inference for %s" % name)
        # cv2.imshow(name, image)
        # cv2.waitKey(1)
        # cv2.destroyAllWindows()
