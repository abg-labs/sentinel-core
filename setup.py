from setuptools import setup, find_packages

setup(
    name="sentinel-core",
    version="0.1.0",
    description="The foundational framework for mission-critical surveillance and situational awareness.",
    author="AB Group",
    author_url="https://abgroupglobal.com",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "opencv-python-headless",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Video :: Capture",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires='>=3.8',
)
