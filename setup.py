from setuptools import setup, find_packages

setup(
    name="mapillary_downloader",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "typing-extensions>=3.7.4",
        "python-dotenv>=0.19.0",
    ],
    entry_points={
        "console_scripts": [
            "mapillary-download=scripts.download_bbox:main",
        ],
    },
    author="Anis Sarker",
    description="A Mapillary image downloader for spatial research segments.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ansarker/mapillary-downloader",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)