# Korean Font Subset Maker

↑ Sorry, I am not good at English or naming. (Also it was unworthy)

## What is this?

Generates subset fonts and CSS file based on [Google Fonts + Korean](https://googlefonts.github.io/korean/).

## How to use

1. Requires [Python](https://www.python.org/downloads/) 3.6 or later.

2. Also it requires [FontTools](https://github.com/fonttools/fonttools); install it with pip:

    ```
    pip3 install fonttools
    ```

3. Clone the project and `cd` into the directory.

    ```
    git clone https://github.com/laziu/KR-font-subset-maker.git
    cd KR-font-subset-maker
    ```

4. It needs sample font CSS file to work, it should contains bunch of seperated `unicode-range`.

    `sample.css` is the part of [`Nanum+Myeongjo:400`](https://fonts.googleapis.com/css?family=Nanum+Myeongjo:400); you can found it from [Google Fonts + Korean](https://googlefonts.github.io/korean/).

5. Download original font files in `assets`.

6. Set appropriate config in `run.py`: 

    ```python
    class path:
      assets = "./assets"
      css    = "./public/css"
      subset = "./public/fonts"
      dest = "/fonts"
      reference = "sample.css"

    fonts = [
      # usage: FontInfo(font_name, font_weight, otf_file, ttf_file)
      FontInfo("KoPub Batang", 300,
               "KOPUB_OTF_FONTS/KoPub Batang_Pro Light.otf", 
               "KOPUB_TTF_FONTS/KoPub Batang Light.ttf"),
      FontInfo("KoPub Batang", 700, 
               "KOPUB_OTF_FONTS/KoPub Batang_Pro Bold.otf",
               "KOPUB_TTF_FONTS/KoPub Batang Bold.ttf")
    ]
    ```

7. You can run now!

    ```
    ./run.py
    ```