import setuptools

setuptools.setup(
    name="bundle",
    version="0.0.1",
    author="David Brochart",
    author_email="david.brochart@gmail.com",
    description="FPGA architecture for array computing",
    long_description="An architecture to process array computing in hardware (typically in an FPGA).",
    long_description_content_type="text/markdown",
    url="https://github.com/davidbrochart/bundle",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
