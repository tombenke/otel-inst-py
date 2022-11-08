from setuptools import find_packages, setup
import pathlib
import os

# Package metadata
# ----------------

NAME = "otel-inst-py"
DESCRIPTION = "Python package that provides the basic features required for Open-Telemetry instrumentation."

# Get the long description from the README file
HERE = pathlib.Path(__file__).parent.resolve()
# LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding="utf-8")
LONG_DESCRIPTION = """
For further information, please visit the [project's homepage](https://github.com/tombenke/otel-inst-py).
"""

URL = "https://github.com/tombenke/otel-inst-py"
EMAIL = "tombenke@gmail.com"
AUTHOR = "Tamás Benke"
LICENSE = "MIT"
REQUIRES_PYTHON = ">=3.8"

# What packages are required for this module to be executed?
REQUIRED = [
    "opentelemetry-api",
    "opentelemetry-sdk",
    "opentelemetry-exporter-otlp-proto-grpc",
    "opentelemetry-exporter-otlp-proto-http",
]

DEV_REQUIREMENTS = [
    "build",
    "coverage",
    "coverage-badge",
    "black",
    "pylint",
    "pdoc",
    "pydeps",
    "python-dotenv",
]

setup(
    name=NAME,
    version=os.getenv("VERSION", "1.0.0"),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    license=LICENSE,
    packages=find_packages(exclude=("tests", "docs")),
    include_package_data=True,
    install_requires=REQUIRED,
    extras_require={"dev": DEV_REQUIREMENTS},
    entry_points={
        "console_scripts": [],
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
