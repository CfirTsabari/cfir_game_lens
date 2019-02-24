"""
East Text detection
"""
import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
from cfir_game_lens.utils import Box, GameCoverImage, ImageSize
from dataclasses import astuple


class EAST:  # pylint: disable=too-few-public-methods
    """East Class
    """

    LAYER_NAMES = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]
    EAST_MODEL_FILE = "frozen_east_text_detection.pb"
    SCALE_FACTOR = 1.0
    MEAN_SUBSTRACTION = (123.68, 116.78, 103.94)
    MIN_CONFIDENCE = 0.5

    def __init__(self):
        self._net = cv2.dnn.readNet(self.EAST_MODEL_FILE)

    @classmethod
    def _resize_image(cls, img: GameCoverImage):
        new_size = ImageSize()
        new_size.height = round(img.size.height / 32) * 32
        new_size.width = round(img.size.width / 32) * 32
        new_img = GameCoverImage(img=cv2.resize(img.img, new_size.get_rev_tuple()))
        return new_img

    def _get_blob(self, img: GameCoverImage):
        blob_args = [img.img, self.SCALE_FACTOR, img.size.get_rev_tuple(), self.MEAN_SUBSTRACTION]
        blob = cv2.dnn.blobFromImage(*blob_args, swapRB=True, crop=False)
        return blob

    @classmethod
    def _build_box(cls, offset_x, offset_y, angle, loc_data):
        (offset_x, offset_y) = (offset_x * 4.0, offset_y * 4.0)
        cos = np.cos(angle)
        sin = np.sin(angle)
        height = loc_data[0] + loc_data[2]
        width = loc_data[1] + loc_data[3]
        end_x = int(offset_x + (cos * loc_data[1]) + (sin * loc_data[2]))
        end_y = int(offset_y - (sin * loc_data[1]) + (cos * loc_data[2]))
        start_x = int(end_x - width)
        start_y = int(end_y - height)
        res = Box(start_x, start_y, end_x, end_y)
        return res

    def _build_boxes(self, scores, geometry):
        boxes = []
        confidences = []
        (num_rows, num_cols) = scores.shape[2:4]
        for y in range(0, num_rows):  # pylint: disable=invalid-name
            # extract the scores (probabilities), followed by the
            # geometrical data used to derive potential bounding box
            # coordinates that surround text
            scores_data = scores[0, 0, y]
            loc_data_arr = [geometry[0, 0, y], geometry[0, 1, y], geometry[0, 2, y], geometry[0, 3, y]]
            angles_data = geometry[0, 4, y]

            # loop over the number of columns
            for x in range(0, num_cols):  # pylint: disable=invalid-name
                if scores_data[x] < self.MIN_CONFIDENCE:
                    continue
                loc_data_arr_x = [loc_data[x] for loc_data in loc_data_arr]
                box = self._build_box(x, y, angles_data[x], loc_data_arr_x)
                boxes.append(box)
                confidences.append(scores_data[x])
        return boxes, confidences

    def find_text(self, image: GameCoverImage):
        """Find boxes of text in image

        Arguments:
            image {GameCoverImage} -- [description]

        Returns:
            List[Box] -- Boxes with text
        """
        # run east model
        resized_img = self._resize_image(image)
        self._net.setInput(self._get_blob(resized_img))
        (scores, geometry) = self._net.forward(self.LAYER_NAMES)

        # create boxes from east output and filter according to confidences\scores
        boxes, confidences = self._build_boxes(scores, geometry)
        boxes_as_tuple = [astuple(x) for x in boxes]
        boxes = non_max_suppression(np.array(boxes_as_tuple), probs=confidences)
        boxes_res = [Box(*x) for x in boxes]

        # fix  images ratio
        ratio_width = image.size.width / float(resized_img.size.width)
        ratio_height = image.size.height / float(resized_img.size.height)
        for box in boxes_res:
            box.fix_sizes(ratio_width, ratio_height)
        return boxes_res
