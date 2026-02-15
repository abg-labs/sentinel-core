from setuptools import setup, find_packages

setup(
    name="sentinel-core",
    version="0.5.0",
    description="The foundational framework for mission-critical surveillance and situational awareness.",
    author="AB Labs",
    author_url="https://github.com/abg-labs/sentinel-core",
    packages=find_packages(include=['ai', 'camera', 'core', 'ai.*', 'camera.*', 'core.*']),
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
