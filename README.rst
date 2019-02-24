cfir_game_lens
==============

A tool that analyze game covers using OpenCV

Usage
-----

`__main__.py folder-read [OPTIONS] FOLDER`

or 
`__main__.py image-read [OPTIONS] FILE`


Requirements
------------
**Tesseract 4.0** [Install from here](https://github.com/UB-Mannheim/tesseract/wiki)
Make sure to add the Tesseract binary folder to the `PATH` env var.
Usually is here: `C:\Program Files (x86)\Tesseract-OCR`

**Dont forget** to install the `requirements.txt` file

**Download** [frozen_east_text_detection.pb](https://github.com/UB-Mannheim/tesseract/wiki) and put it in the root directory

Compatibility
-------------
Tested on python 3.7 on windows.

Licence
-------

Authors
-------

`cfir_game_lens` was written by `Cfir Tsabari <cfir.tsabari@gmail.com>`_.
