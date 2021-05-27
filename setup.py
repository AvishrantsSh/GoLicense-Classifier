import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testpkg_avishrantssh",
    version="0.0.1",
    author="AvishrantSh (Avishrant Sharma)",
    author_email="<avishrants@gmail.com>",
    description="A Python based License Classifier",
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
    package_data={'': ['py_my_lib.so']},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)