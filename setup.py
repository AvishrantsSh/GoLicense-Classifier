import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="golicense_classifier",
    version="0.0.4",
    author="AvishrantSh (Avishrant Sharma)",
    author_email="<avishrants@gmail.com>",
    description="A Python based License Classifier based on Google License Classifier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AvishrantsSh/LicensePackage",
    project_urls={
        "Bug Tracker": "https://github.com/AvishrantsSh/LicensePackage/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    package_dir={"": "src"},
    include_package_data=True,
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
