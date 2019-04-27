import click
import os
import re


@click.command(options_metavar='[options]',
               context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(version='0.1.0')
@click.option('-o', '--output', metavar='<file>',
              type=click.Path(exists=False, dir_okay=False, resolve_path=True),
              default=lambda: os.path.join(os.getcwd(), 'output.tar.gz'),
              help='The output archive file path.')
@click.option('-n', '--name', metavar='<text>', type=click.STRING,
              help='font-name of output fonts.  [default: <font-file>]')
@click.option('-f', '--format', metavar='<text>[,..]',
              default='woff2,woff', show_default=True,
              help='font-formats of output fonts.')
@click.option('-w', '--weight', metavar='<int>',
              default=400, show_default=True,
              help='font-weight of output fonts.')
@click.argument('font_file', metavar='<font-file>',
                type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def krwftgen(output, name, format, weight, font_file):
    """\
    krwftgen -- Korean webfont generator

    \b
    krwftgen generates korean webfonts splitted into individual unicode-range
    to make big-webfont rendering faster and more efficiently.
    It is inspired by Google Fonts + Korean, which provides korean webfonts
    splitted download using machine learning.
    """
    if name is None:
        _, name = os.path.split(font_file)
        name = re.sub(r'\.(ttf|otf|woff|woff2)$', '', name)
        name = re.sub(r'[^A-Za-z]*', '', name)

    print(output, name, format, weight, font_file)
