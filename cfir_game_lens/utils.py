"""
Utils-data classes
"""

from typing import Any
import cv2
from dataclasses import dataclass, field, astuple

# pylint: disable=missing-docstring


@dataclass
class Box:
    start_x: float
    start_y: float
    end_x: float
    end_y: float

    def fix_sizes(self, ratio_width, ratio_height):
        self.start_x = int(self.start_x * ratio_width)
        self.start_y = int(self.start_y * ratio_height)
        self.end_x = int(self.end_x * ratio_width)
        self.end_y = int(self.end_y * ratio_height)


@dataclass
class ImageSize:
    height: int = 0
    width: int = 0

    def get_rev_tuple(self):
        return astuple(self)[::-1]


@dataclass
class GameCoverImage:
    file_name: str = ""
    img: Any = None
    size: ImageSize = field(init=False)

    def __post_init__(self):
        if self.file_name:
            self.img = cv2.imread(self.file_name)
        self.size = ImageSize(*self.img.shape[:2])
