import click
import os
import re
import requests
import tempfile
import shutil
import pathlib
from fontTools import ttLib
from fontTools.subset import main as pyftsubset


google_fonts_sample_url = 'https://fonts.googleapis.com/css?family=Nanum+Gothic'
browser_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'


@click.command(options_metavar='[options]',
               context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(version='0.1.0')
@click.option('-n', '--name', metavar='<text>', type=click.STRING,
              help='font-name of output fonts.  [default: <font-file>]')
@click.option('-f', '--format', metavar='<text>[,..]',
              default='woff2,woff', show_default=True,
              help='font-formats of output fonts.')
@click.option('-w', '--weight', metavar='<int>',
              default=400, show_default=True,
              help='font-weight of output fonts.')
@click.option('--style', metavar='<text>',
              default='normal', show_default=True)
@click.argument('font_path', metavar='<font-path>',
                type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def krwftgen(name, format, weight, style, font_path):
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
    esc_name = re.sub(r'\W', "_", name)
    output_path = rel_path(esc_name)

    print(output_path, name, format, weight, style, font_path, esc_name)

    font_info = FontInfo(name, format, weight, style)
    temp_folder = TempFolder()
    out_path = temp_folder.path(f"{esc_name}/{font_info.weight}")
    gen_path(out_path)

    with StyleWriter(font_info, temp_folder) as wb:
        unicode_range_list = unicode_subranges()
        list_len = len(unicode_range_list)
        for i, urange in enumerate(unicode_range_list):
            i_str = "%03d" % i
            print(f'processing ({i_str}/{list_len})')
            make_subset(font_path, out_path, i_str, urange, font_info)
            make_subset(font_path, out_path, i_str,
                        urange, font_info, woff2=True)
            wb.css_write(i_str, urange)
            wb.scss_write(i_str, urange)

    make_zip(output_path, temp_folder.path(f"{esc_name}"))


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


def make_subset(font_path, out_path, index, uni_range, font_info, woff2=False):
    commands = [
        font_path,
        f"--unicodes={uni_range}",
        f"--output-file={out_path}/{index}.{'woff2' if woff2 else 'woff'}",
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
    if woff2:
        commands.append('--flavor=woff2')
    else:
        commands.append('--flavor=woff')
        commands.append('--with-zopfli')
    pyftsubset(commands)


def rel_path(relative_path):
    """Get absolute path from relative path."""
    return os.path.join(os.getcwd(), relative_path)


def gen_path(new_path):
    pathlib.Path(new_path).mkdir(parents=True, exist_ok=True)


def make_zip(out_path, dir_path):
    shutil.make_archive(out_path, 'zip', dir_path)


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


class FontInfo:
    def __init__(self, name, format_list, weight, style):
        self.name = name
        self.esc_name = re.sub(r'\W', "_", name)
        self.format_list = format_list.split(',')
        self.weight = weight
        self.style = style


class StyleWriter:
    def __init__(self, font_info, temp_folder):
        self.font_info = font_info
        self.temp_folder = temp_folder

    def __enter__(self):
        gen_path(self.temp_folder.path(self.font_info.esc_name))
        self.css = open(self.temp_folder.path(
            f"{self.font_info.esc_name}/{self.font_info.weight}.css"), "w")
        self.scss = open(self.temp_folder.path(
            f"{self.font_info.esc_name}/{self.font_info.weight}.scss"), "w")
        self.scss.write(
            ((
                "@mixin font-subset( $index, $range ) {{\n"
                "  @font-face {{\n"
                "    font-family: '{name}';\n"
                "    font-style: {style};\n"
                "    font-weight: {weight}\n"
                "    src: url('{dest}/{name}/{weight}/#{{$index}}.woff2') format('woff2'),\n"
                "         url('{dest}/{name}/{weight}/#{{$index}}.woff' ) format('woff ');\n"
                "    unicode-range: #{{$range}};\n"
                "  }}\n"
                "}}\n\n"
            )).format(
                name=self.font_info.name,
                esc_name=self.font_info.esc_name,
                weight=self.font_info.weight,
                style=self.font_info.style,
                dest="."
            )
        )
        return self

    def __exit__(self, type, value, traceback):
        self.css.close()
        self.scss.close()

    def css_write(self, index, unicode_range):
        self.css.write(
            ((
                "@font-face {{\n"
                "  font-family: '{name}';\n"
                "  font-style: {style};\n"
                "  font-weight: {weight};\n"
                "  src: url('{dest}/{name}/{weight}/{index}.woff2') format('woff2'),\n"
                "       url('{dest}/{name}/{weight}/{index}.woff' ) format('woff' );\n"
                "  unicode-range: {range};\n"
                "}}\n\n"
            )).format(
                name=self.font_info.name,
                esc_name=self.font_info.esc_name,
                weight=self.font_info.weight,
                style=self.font_info.style,
                index=index,
                range=unicode_range,
                dest="."
            )
        )

    def scss_write(self, index, unicode_range):
        self.scss.write(
            f"@include font-subset( '{index}', '{unicode_range}' );\n"
        )
