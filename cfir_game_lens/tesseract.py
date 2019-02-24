"""
Tesseract Text recognition
"""
import abc
from typing import List
import pytesseract
import cv2
from cfir_game_lens.utils import GameCoverImage, Box


class _ImageReducer(abc.ABC):
    def __init__(self, *args, reducer=None, weight=0.0, **kwargs):
        _ = args
        _ = kwargs
        self._reducer = reducer
        self._weight = weight

    def reduce(self, img):
        """Return image after changing it

        Arguments:
            img {Image} -- Image

        Returns:
            image -- Image
        """

        res = self._reduce(img)
        if self._weight:
            cv2.addWeighted(img, 1 - self._weight, res, self._weight, 0)
        if self._reducer:
            res = self._reducer.reduce(res)
        return res

    def set_reducer(self, reducer):
        """Set reducer

        Arguments:
            reducer {_ImageReducer} -- image reducer
        """

        self._reducer = reducer

    @abc.abstractmethod
    def _reduce(self, img):
        pass


class _VoidReducer(_ImageReducer):
    def _reduce(self, img):
        return img


class _BitWiseReducer(_ImageReducer):
    def _reduce(self, img):
        return cv2.bitwise_not(img)


class _MedianBlurReducer(_ImageReducer):
    def __init__(self, *args, **kwargs):
        super(_MedianBlurReducer, self).__init__(*args, **kwargs)
        self.blur_level = kwargs.get("blur_level", 3)

    def _reduce(self, img):
        return cv2.medianBlur(img, self.blur_level)


class _GaussianBlurReducer(_ImageReducer):
    def _reduce(self, img):
        return cv2.GaussianBlur(img, (3, 3), 0)


class _GrayReducer(_ImageReducer):
    def _reduce(self, img):
        res = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        res = cv2.threshold(res, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        return res


# gray = cv2.addWeighted(cover.img, 0.7, gray, 0.3, 0)


class Tesseract:  # pylint: disable=too-few-public-methods
    """
    Tesseract class
    """

    CONFIG = "-l eng --oem 1 --psm 7"
    PADDING = 0.010

    @classmethod
    def _build_reducers(cls):
        return [
            # (BitWiseReducer(GrayReducer(MedianBlurReducer())), 'first'),
            # (BitWiseReducer(GrayReducer(MedianBlurReducer(blur_level=5))), 'second'),
            # (BitWiseReducer(GrayReducer(MedianBlurReducer(blur_level=9))), 'third'),
            # (GrayReducer(MedianBlurReducer(BitWiseReducer(), blur_level=3)), 'forth'),
            # (GrayReducer(MedianBlurReducer(blur_level=3)), 'five'),
            (_BitWiseReducer(weight=0.3), "six"),
            (_BitWiseReducer(_GaussianBlurReducer(), weight=0.3), "g"),
        ]

    def read_text(self, image: GameCoverImage, boxes: List[Box]):
        """Read text from image according to boxes.

        Arguments:
            image {GameCoverImage} -- source image
            boxes {List[Box]} -- boxes of text
        """
        reducers = self._build_reducers()
        results = []
        for reducer, _ in reducers:
            temp_results = []
            # change image according to predefine methods
            reduced_image = reducer.reduce(image.img)
            for box in boxes:
                # Add padding
                padding_x = int((box.end_x - box.start_x) * self.PADDING)
                padding_y = int((box.end_y - box.start_y) * self.PADDING)
                box.start_x = max(0, box.start_x - padding_x)
                box.start_y = max(0, box.start_y - padding_y)
                box.end_x = min(image.size.width, box.end_x + padding_x)
                box.end_y = min(image.size.height, box.end_y + padding_y)
                roi = reduced_image[box.start_y : box.end_y, box.start_x : box.end_x]

                # get text using tesseract
                text = pytesseract.image_to_string(roi, config=self.CONFIG)
                temp_results.append(text)

            results.append(temp_results)
        return results
