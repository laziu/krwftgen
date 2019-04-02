import re
import pathlib

# utils


def readlines(filename):
    with open(filename, "r") as file:
        return file.readlines()


def get_unicode_range_from_css(lines):
    unicodes = []
    for line in lines:
        if "unicode-range" in line:
            unicodes.append(re.sub(r'[;\s]', "", line.split(":")[1]))
    return unicodes


def generate_path(new_path):
    pathlib.Path(new_path).mkdir(parents=True, exist_ok=True)


# helper classes
class FontInfo:
    def __init__(self, name, size, orig, ttf=None):
        self.name = name
        self.size = size
        self.orig = orig
        self.ttf = ttf


class FontCssFile:
    def __init__(self, font, file, dest_path):
        self.font = font
        self.file = file
        self.dest_path = dest_path

    def write(self, i, unicode_range):
        self.file.write(
            ((
                "@font-face {{\n"
                "  font-family: '{name}';\n"
                "  font-style: normal;\n"
                "  font-weight: {size};\n"
                "  src: url('{dest}/{name}-{size}/{index:02d}.woff2') format('woff2'),\n"
                "       url('{dest}/{name}-{size}/{index:02d}.woff') format('woff')"
            ) + (
                ",\n       url('{dest}/{name}-{size}/{index:02d}.ttf') format('truetype')"
                if self.font.ttf is not None else ""
            ) + (
                ";\n"
                "  unicode-range: {range};\n"
                "}}\n\n"
            )).format(
                name=self.font.name,
                size=self.font.size,
                index=i,
                range=unicode_range,
                dest=self.dest_path
            )
        )


class Command:
    def __init__(self, font_path, subset_path):
        self.font_path = font_path
        self.subset_path = subset_path
        self.font = None
        self.unicode_range = None
        self.i = None
        self.ftype = None

    def setFont(self, font):
        self.font = font
        return self

    def setRangeWithIndex(self, unicode_range, i):
        self.unicode_range = unicode_range
        self.i = i
        return self

    def setFontType(self, ftype):
        self.ftype = ftype
        return self

    def get(self):
        assert self.font is not None
        assert self.unicode_range is not None
        assert self.i is not None
        assert self.ftype is not None
        commands = [
            'pyftsubset',
            '{font_path}/{font_file}',
            '--unicodes={unicode_range}',
            '--output-file={subset_path}/{font_name}-{font_size}/{index:02d}.{ext}',
            "--layout-features='*'",
            "--glyph-names",
            "--symbol-cmap",
            "--legacy-cmap",
            "--notdef-glyph",
            "--notdef-outline",
            "--recommended-glyphs",
            "--name-legacy",
            "--drop-tables=",
            "--name-IDs='*'",
            "--name-languages='*'"
        ]
        if self.ftype == 'woff2':
            commands.append('--flavor=woff2')
        elif self.ftype == 'woff':
            commands.append('--flavor=woff')
            commands.append('--with-zopfli')

        return [cmd.format(
            font_path=self.font_path,
            font_file=(self.font.ttf if self.ftype ==
                       'ttf' else self.font.orig),
            unicode_range=self.unicode_range,
            subset_path=self.subset_path,
            font_name=self.font.name,
            font_size=self.font.size,
            index=self.i,
            ext=self.ftype
        ) for cmd in commands]
