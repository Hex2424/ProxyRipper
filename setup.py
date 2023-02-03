from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1.4'
DESCRIPTION = 'Tool for scrapping valid proxies'
LONG_DESCRIPTION = 'A Python application for scrapping proxies from online Proxy Sites and checking their validity'

# Setting up
setup(
    name="ProxyRipper",
    version=VERSION,
    author="Hex24 (Markas Vielavičius)",
    author_email="<markas.vielavicius@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
package_dir={"ProxyRipper": "ProxyRipper"},
include_package_data=True,   
 install_requires=['requests==2.25.1', 'validators==0.20.0'],
    keywords=['python', 'proxy', 'scrapper', 'ripper', 'api', 'proxies'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        'console_scripts': [
            'ProxyRipper=ProxyRipper.ProxyRipper:main',
        ],
    }
)
