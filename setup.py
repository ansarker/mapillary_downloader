from setuptools import setup, find_packages

setup(
    name="mapillary_downloader",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
    ],
    entry_points={
        "console_scripts": [
            "mapillary-download=scripts.download_bbox:main",
        ],
    },
)