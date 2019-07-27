from setuptools import setup, find_packages

setup(
    name='krwftgen',
    version='0.1',
    description='Korean webfont generator using Google Fonts + Korean',
    author='Laziu Kim',
    author_email='laziu.cc@gmail.com',
    url='https://github.com/laziu/krwftgen',
    download_url='https://github.com/laziu/krwftgen/archive/0.1.tar.gz',
    zip_safe=False,
    python_requires='>=3.4',
    install_requires=[
        'fonttools==3.39.0',
        'brotli==1.0.7; platform_python_implementation != "PyPy"',
        'brotlipy==0.7.0; platform_python_implementation == "PyPy"',
        'zopfli==0.1.6',
        'requests==2.21.0'
    ],
    setup_requires=[
        'autopep8==1.4.3',
        'pylint==2.3.1',
        'docutils==0.14'
    ],
    packages=find_packages('Lib'),
    package_data={},
    entry_points={
        'console_scripts': [
            'krwftgen = Lib.__init__:krwftgen'
        ]
    },
    keywords=[
        'krwftgen',
        'fonttools'
    ],
    classifiers=[
        'Topic :: Text Processing :: Fonts',
        'Natural Language :: Korean'
    ]
)
