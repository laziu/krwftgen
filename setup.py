from setuptools import setup, find_packages

setup(
    name='krftsubset',
    version='0.1',
    description='Korean font substractor using Google Fonts + Korean',
    author='Laziu Kim',
    author_email='laziu.cc@gmail.com',
    url='https://github.com/laziu/krftsubset',
    download_url='https://github.com/laziu/krftsubset/archive/???',
    install_requires=[
        'fonttools==3.39.0',
        'brotli==1.0.7; platform_python_implementation != "PyPy"',
        'brotlipy==0.7.0; platform_python_implementation == "PyPy"',
        'zopfli==0.1.6',
        'requests==2.21.0'
    ],
    packages=find_packages('Lib'),
    classifiers=[
        'Topic :: Text Processing :: Fonts',
        'Natural Language :: Korean'
    ]
)
