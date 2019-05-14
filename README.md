** ※ 완성되지 않은 프로젝트입니다. ※ **

## 이게 뭔가요?

한글 폰트를 [fonttools](https://github.com/fonttools/fonttools)를 이용해
[Google Fonts + 한국어](https://googlefonts.github.io/korean/)처럼 분할해주는 툴입니다.

## 개발환경 설정

```bash
git clone https://github.com/laziu/krwftgen.git
cd krwftgen
python -m venv .venv            # >= 3.4
source .venv/bin/activate       # cmd: '.venv/bin/activate.bat'
python -m pip install -r requirements.txt
python -m pip install -r dev-requirements.txt
python -m pip install --editable .
```
