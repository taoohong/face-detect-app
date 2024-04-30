import logging
import os
import cv2
import numpy as np
import time

from anti_spoofing.src.anti_spoof_predict import AntiSpoofPredict
from anti_spoofing.src.generate_patches import CropImage
from anti_spoofing.src.utility import parse_model_name

cur_dir = os.path.dirname(__file__)
model_dir = cur_dir + "/models/anti_spoof_models"


# 限制图片长宽比4:3
def check_image(image):
    height, width, channel = image.shape
    if width / height != 8 / 5:
        logging.error("Image is not appropriate!!!\nHeight/Width should be 8/5.")
        return False
    else:
        return True


class FaceAntiSpoof:
    def __init__(self, device_id=0):
        self.model = AntiSpoofPredict(device_id)
        self.image_cropper = CropImage()

    def detect(self, image):
        if not check_image(image):
            return image
        image_bbox = self.model.get_bbox(image)
        prediction = np.zeros((1, 3))
        test_speed = 0
        # sum the prediction from single model's result
        for model_name in os.listdir(model_dir):
            h_input, w_input, model_type, scale = parse_model_name(model_name)
            param = {
                "org_img": image,
                "bbox": image_bbox,
                "scale": scale,
                "out_w": w_input,
                "out_h": h_input,
                "crop": True,
            }
            if scale is None:
                param["crop"] = False
            img = self.image_cropper.crop(**param)
            start = time.time()
            prediction += self.model.predict(img, os.path.join(model_dir, model_name))
            test_speed += time.time() - start

        # draw result of prediction
        label = np.argmax(prediction)
        value = prediction[0][label] / 2
        if label == 1:
            logging.info("Image is Real Face. Score: {:.2f}.".format(value))
            result_text = "RealFace Score: {:.2f}".format(value)
            color = (0, 0, 255)
        else:
            logging.info("Image is Fake Face. Score: {:.2f}.".format(value))
            result_text = "FakeFace Score: {:.2f}".format(value)
            color = (255, 0, 0)
        logging.info("Prediction cost {:.2f} s".format(test_speed))
        cv2.rectangle(
            image,
            (image_bbox[0], image_bbox[1]),
            (image_bbox[0] + image_bbox[2], image_bbox[1] + image_bbox[3]),
            color, 2)
        cv2.putText(
            image,
            result_text,
            (image_bbox[0], image_bbox[1] - 5),
            cv2.FONT_HERSHEY_COMPLEX, 0.5, color)
        return image, label == 1
