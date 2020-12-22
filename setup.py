"""Setup."""

from pathlib import Path

from setuptools import find_packages, setup

THIS_DIRECTORY = Path(__file__).resolve().parent

# I looked and could not find an old version without the API we need,
# so not going to condition on a version.
INSTALL_REQUIRES = ["scipy", "numpy"]

# use readme as long description
LONG_DESCRIPTION = (THIS_DIRECTORY / "readme.md").read_text()

setup(
    name="binoculars",
    version="0.1.0",
    description="Various calculations for binomial confidence intervals.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Nolan Conaway",
    author_email="nolanbconaway@gmail.com",
    url="https://github.com/nolanbconaway/binoculars",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords=["statistics", "binomial", "confidence"],
    license="MIT",
    package_dir={"": "lib"},
    packages=find_packages("lib"),
    install_requires=INSTALL_REQUIRES,
    extras_require=dict(
        test=["black==20.8b1", "pytest==6.2.1", "pytest-cov==2.10.1", "codecov==2.1.11"]
    ),
    package_data={"shabadoo": ["version"]},
)
