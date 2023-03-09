import warnings
from setuptools import setup, find_packages

warnings.filterwarnings('ignore')

setup(
    name="evtool",
    version="1.0.0",
    author="Kuga",
    author_email="KugaMaxx@outlook.com",
    description="a generic and simple toolkit for processing event-based data",
    url="https://github.com/KugaMaxx/event-camera-toolkit",
    packages=find_packages(where='src'),
    package_dir={'':'src'},
    install_requires=[
        'argparse',
        'dv>=1.0.10',
        'pint>=0.20.1',
        'numpy>=1.23.5',
        'scipy>=1.10.1',
        'plotly>=5.9.0',
        'pandas>=1.5.2',
        'matplotlib>=3.6.2',
        'opencv-python>=4.7.0.68',
    ],
)
