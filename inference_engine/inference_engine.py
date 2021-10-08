import logging
import threading
from queue import Queue

import cv2
import numpy as np
from pupil_apriltags import Detector

from inference_engine.inference_entities import AprilTag, Vehicle, InferenceResult


class Image:

    def __init__(self, name, img_bytes):
        self.name = name
        self.cv2_image = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), -1)


class InferenceEngine(threading.Thread):

    def __init__(self, inference_callback=None):
        super().__init__()
        self.img_queue = Queue()
        self.inference_callback = inference_callback

    def queue_img(self, data, name):
        image = Image(name, data)
        self.img_queue.put(image)

    def run(self) -> None:
        logging.debug("Running Inference")
        while True:
            while not self.img_queue.empty():
                img = self.img_queue.get()
                _ = self.make_inference(img.cv2_image, img.name, self.inference_callback)
                window_name = "Running Inference Engine @ " + str(self.get_camera_name(img.name))
                # cv2.imshow(window_name, img.cv2_image)
                # cv2.waitKey(1)
                # time.sleep(1)
            # cv2.destroyAllWindows()

    @staticmethod
    def to_numpy(img_bytes):
        logging.debug("converting image to numpy array")
        return cv2.imdecode(np.frombuffer(img_bytes, np.uint8), -1)

    @staticmethod
    def make_inference(cv2_image, image_name='default-name', callback=None, **kwargs) -> dict:
        logging.info("Making inference for %s" % image_name)
        april_tags_result = InferenceEngine.detect_april_tags(cv2_image)
        vehicles_result = InferenceEngine.detect_vehicles()
        # inference_engine_package = DictTool.to_dict(DictTool.join_dicts(april_tags_result, vehicles_result))
        cam_id, timestamp, metadata = InferenceEngine.parse_image_name(image_name)

        # Dummy Values for testing purposes
        apriltag1 = AprilTag(1, (1, 2, 3, 4))
        apriltag2 = AprilTag(2, (2, 3, 4, 5))
        vehicle1 = Vehicle(0.98, (1, 2, 6, 7))
        vehicle2 = Vehicle(0.88, (3, 4, 8, 8))
        inference_result = InferenceResult([apriltag1, apriltag2], [vehicle1, vehicle2])
        inference_engine_package = {'cam_id': cam_id,
                                    'timestamp': timestamp,
                                    'metadata': metadata,
                                    'inference_result': inference_result.to_json()}
        if callback:
            callback(inference_engine_package, **kwargs)

        logging.debug("Inference Result: %s" % str(inference_engine_package))
        return inference_engine_package

    @staticmethod
    def parse_image_name(img_name: str) -> tuple:
        content = img_name.replace(".jpg", "").replace(".png", "").split('_')
        if len(content) > 3:
            cam_id = content[0]
            timestamp = content[2]
            metadata = str(content[3:])
            return cam_id, timestamp, metadata
        return "Unknown", "Unknown", "Nothing"

    @staticmethod
    def get_camera_name(img_name: str):
        content = img_name.split('_')
        logging.debug(content[0])
        return content[0] if len(content) > 0 else "Unknown_Camera"

    @staticmethod
    def detect_april_tags(cv2_image) -> dict:
        # tag families: tag36h11
        at_detector = Detector(families='tag16h5', quad_sigma=0.1, quad_decimate=1.0)
        img_copy = cv2_image

        # smooth image for a better apriltag detection
        blur_img = cv2.blur(img_copy, (7, 7))

        # apriltag images need to be in grayscale
        gray_img = cv2.cvtColor(blur_img, cv2.COLOR_BGR2GRAY)

        tags = at_detector.detect(gray_img, estimate_tag_pose=False, camera_params=None, tag_size=None)

        # This is for debugging purposes
        # cv2.imshow("blur image", blur_img)
        # cv2.imshow("gray image", gray_img)

        for tag in tags:
            logging.info("found tag_id %s" % tag.tag_id)
            for idx in range(len(tag.corners)):
                cv2.line(
                    cv2_image,
                    tuple(tag.corners[idx - 1, :].astype(int)),
                    tuple(tag.corners[idx, :].astype(int)),
                    (255, 0, 0),
                    thickness=2,
                )

            cv2.putText(
                cv2_image,
                "id:" + str(tag.tag_id),
                org=(
                    tag.corners[0, 0].astype(int) + 10,
                    tag.corners[0, 1].astype(int) + 10,
                ),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=(0, 255, 0),
                thickness=2,
            )

            result = {'apriltag_result': "Dummy_Value"}
            return result

    @staticmethod
    def detect_vehicles() -> dict:
        result = {'vehicles_result': "Dummy_Value"}
        return result
