from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = "Clinic Description Annotator"
LONG_DESCRIPTION = "An annotator for people easily annotate clinic descriptions."

setup(
    # the name must match the package name - verysimpletest
    name="digitaltwin description annotator for Sparc dataset",
    version=VERSION,
    author="LinkunGao",
    author_email="gaolinkun123@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    # Add any packages if you use it in your packages
    install_requires=[],
    keywords=['python', 'test'],
    classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "License :: OSI Approved :: Apache Software License"
    ]
)