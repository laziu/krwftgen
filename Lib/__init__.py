import click
import os
import re
import requests
import tempfile
import shutil
from fontTools import ttLib
from fontTools.subset import main as pyftsubset


google_fonts_sample_url = 'https://fonts.googleapis.com/css?family=Nanum+Gothic'
browser_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'


@click.command(options_metavar='[options]',
               context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(version='0.1.0')
@click.option('-o', '--output', 'output_path', metavar='<file>',
              type=click.Path(exists=False, dir_okay=False, resolve_path=True),
              default=lambda: rel_path('output.tar.gz'),
              help='The output archive file path.')
@click.option('-n', '--name', metavar='<text>', type=click.STRING,
              help='font-name of output fonts.  [default: <font-file>]')
@click.option('-f', '--format', metavar='<text>[,..]',
              default='woff2,woff', show_default=True,
              help='font-formats of output fonts.')
@click.option('-w', '--weight', metavar='<int>',
              default=400, show_default=True,
              help='font-weight of output fonts.')
@click.argument('font_path', metavar='<font-path>',
                type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def krwftgen(output_path, name, format, weight, font_path):
    """\
    krwftgen -- Korean webfont generator

    \b
    krwftgen generates korean webfonts splitted into individual unicode-range
    to make big-webfont rendering faster and more efficiently.
    It is inspired by Google Fonts + Korean, which provides korean webfonts
    splitted download using machine learning.
    """
    if name is None:
        name = get_font_family_name(font_path)

    print(output_path, name, format, weight, font_path)

    temp = TempFolder()

    pyftsubset([font_path,
                "--unicodes=U+d723-d728,U+d72a-d733,U+d735-d748,U+d74a-d74f,U+d752-d753,U+d755-d757,U+d75a-d75f,U+d762-d764,U+d766-d768,U+d76a-d76b,U+d76d-d76f,U+d771-d787,U+d789-d78b,U+d78d-d78f,U+d791-d797,U+d79a,U+d79c,U+d79e-d7a3,U+f900-f909,U+f90b-f92e",
                "--output-file=%s" % temp.path("sample_output.ttf"),
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
                "--name-languages='*'"])


def get_font_family_name(font_path):
    """Get font family name of font file. Input is path of font"""
    for record in ttLib.TTFont(font_path)['name'].names:
        if record.nameID == 1:      # FAMILY SPECIFIER ID
            return record.string.decode('utf-16-be' if b'\x00' in record.string else 'utf-8')


def unicode_subranges():
    """List of unicode sub-ranges in Google Fonts Korean CSS."""
    unicodes = []
    result = requests.get(google_fonts_sample_url, headers={
        'User-Agent': browser_agent
    })
    for line in result.content.decode('utf-8').splitlines():
        if "unicode-range" in line:
            unicodes.append(re.sub(r'[;\s]', "", line.split(":")[1]))
    return unicodes


def rel_path(relative_path):
    """Get absolute path from relative path."""
    return os.path.join(os.getcwd(), relative_path)


class TempFolder:
    def __init__(self):
        """Clear temporary folder."""
        self.root = os.path.join(tempfile.gettempdir(), "krwftgen")
        if os.path.exists(self.root):
            shutil.rmtree(self.root)
        os.makedirs(self.root)

    def path(self, relative_path):
        """Get temporary path from relative path."""
        return os.path.join(self.root, relative_path)
