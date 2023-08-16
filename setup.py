import os
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(os.path.join("src", "peakrdl_cheader", "__about__.py")) as f:
    v_dict = {}
    exec(f.read(), v_dict)
    version = v_dict['__version__']

setup(
    name="peakrdl-cheader",
    version=version,
    author="Keith Brady",
    description="Generate c headers for register model compiled SystemRDL input",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krcb197/PeakRDL-CHeader",
    package_dir={'': 'src'},
    packages=[ 'peakrdl_cheader'],
    package_data={"peakrdl_cheader.templates": ["*.h.jinga"]},
    include_package_data = True,
    entry_points= { 'console_scripts' : ['peakrdl_cheader=peakrdl_cheader.peakcheader:main_function'] },
    install_requires=[
        "systemrdl-compiler>=1.21.0",
        "jinja2",
        "peakrdl-ipxact"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
    project_urls={
        "Source": "https://github.com/krcb197/PeakRDL-cheader",
        "Tracker": "https://github.com/krcb197/PeakRDL-cheader/issues",
        "Documentation": "https://peakrdl-cheader.readthedocs.io/"
    },
)
