from fontTools.subset import main as pyftsubset
import os
import re
import requests

url = 'https://fonts.googleapis.com/css?family=Nanum+Gothic'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
r = requests.get(url, headers=headers)

unicodes = []
for line in r.content.decode('ascii').splitlines():
    if "unicode-range" in line:
        unicodes.append(re.sub(r'[;\s]', "", line.split(":")[1]))

for u in unicodes:
    print(u)


def getpath(file):
    path, _ = os.path.split(__file__)
    return os.path.join(path, "data", file)


pyftsubset([getpath("IropkeBatangM.ttf"),
            "--unicodes=U+d723-d728,U+d72a-d733,U+d735-d748,U+d74a-d74f,U+d752-d753,U+d755-d757,U+d75a-d75f,U+d762-d764,U+d766-d768,U+d76a-d76b,U+d76d-d76f,U+d771-d787,U+d789-d78b,U+d78d-d78f,U+d791-d797,U+d79a,U+d79c,U+d79e-d7a3,U+f900-f909,U+f90b-f92e",
            "--output-file=%s" % getpath("sample_output.ttf"),
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
