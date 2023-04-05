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
        'pint',
        'numpy==1.23.5',
        'numba==0.56.4',
        'scipy',
        'plotly',
        'pandas',
        'matplotlib',
        'opencv-python',
        'dv==1.0.10',
    ],
)
