"""
Cfir Game Lens CLI
"""
import os
import click
import cv2
from cfir_game_lens.utils import GameCoverImage
from cfir_game_lens.east import EAST
from cfir_game_lens.tesseract import Tesseract

CONSOLES = {"PC": ["pc"], "XBOX-ONE": ["xboxone", "xbox"], "PS4": ["ps4", "ps"]}


@click.group()
def main():
    """
    Main entry
    """


@main.command()
@click.argument("folder", type=click.Path(exists=True))
def folder_read(folder):
    """
    Read images from folder and print game title and game platform
    """
    files_path = [os.path.join(folder, x) for x in os.listdir(folder)]
    for file_name in files_path:
        print(file_name)
        _image_read_helper(file_name, True, True)

    cv2.waitKey(0)


@main.command()
@click.argument("file", type=click.Path(exists=True, readable=True))
def image_read(file):
    """
    Read image file and print game title and game platform
    """
    _image_read_helper(file)


def _image_read_helper(file, wait=True, just_print=False):

    cover = GameCoverImage(file)
    east_model = EAST()
    tesseract_imp = Tesseract()
    boxes = east_model.find_text(cover)
    words = tesseract_imp.read_text(cover, boxes)
    console = _find_console(words)
    if just_print:
        print(console)
    else:
        cv2.imshow(console, cover.img)
        if wait:
            cv2.waitKey(0)


def _find_console(words):
    flat_words = [item.lower() for sublist in words for item in sublist]
    print(words)
    for console, names in CONSOLES.items():
        for name in names:
            for word in flat_words:
                if name in word:
                    return console
    return "Not found"
