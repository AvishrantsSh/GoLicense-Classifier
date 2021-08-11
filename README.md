GoLicense-Classifier
====================

<p>
<img src="https://img.shields.io/pypi/v/golicense_classifier.svg?style=for-the-badge" alt="PyPI Shield">
<img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="MIT License">
<img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge" alt="Code Format">
</p>

___

A Python package to find license expressions and copyright statements in a codebase. 

Based on **Google LicenseClassifer V2**, GoLicense-Classifier (or **glc** for short) focuses on performance without compromising with accuracy.

Installation
------------
_Note: Currently, this package only supports Linux Platform. Work is in progress for Windows and Mac._

Installing GoLicense-Classifier is as simple as
```sh
pip install golicense-classifier
```

Or, you can build the package from source as
```sh
git clone https://github.com/AvishrantsSh/GoLicense-Classifier.git
make dev
make package
```

Usage
-----
To get started, import `LicenseClassifier` class from the module as

```python
from LicenseClassifier.classifier import LicenseClassifier
```

_Note: Work on Copyright Statement is still in beta phase. Expect some issues, mostly with binary files_

The class comes bundled with some handy functions, each suited for a different task.

1. `scan_directory`
        
    This method is used to recursively walk through a directory and find license expressions and copyright statements. It returns a dictionary object with keys `header` and `files`.
    
    ### Usage
    ___
    ```python
    classifier = LicenseClassifier()
    res = classifier.scan_directory('PATH_TO_DIR')
    ```
    ### Optional Parameters
    ___
    - `max_size`
        
        Maximum size of file in MB. Default is set to 10MB. Set `max_size < 0` to ignore size constraints

    - `use_buffer`
        
        `(Experimental)` Set to `True` to use buffered file scanning. `max_size` will be used as buffer size.

    - `use_scancode_mapping`

        Set to `True` if you want to use Scancode license key mappings. Default is set to `True`.

2. `scan_file`

    This method is used to find license expressions and copyright statements in a single file.
    
    ### Usage
    ___
    ```python
    classifier = LicenseClassifier()
    res = classifier.scan_file('PATH_TO_FILE')
    ```
    ### Optional Parameters
    ___
    - `max_size`
        
        Maximum size of file in MB. Default is set to 10MB. Set `max_size < 0` to ignore size constraints

    - `use_buffer`
        
        `(Experimental)` Set to `True` to use buffered file scanning. `max_size` will be used as buffer size.

    - `use_scancode_mapping`

        Set to `True` if you want to use Scancode license key mappings. Default is set to `True`.

Further Customization
---------------------
You can set custom threshold for scanning purpose that best suits your need. Simply change the parameter `threshold` during object creation as
```python
classifier = LicenseClassifier(threshold = 0.9)
```

Contributing
------------
Contributions are what makes the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

To get started, read the [Contributing Guide](CONTRIBUTING.md).

References
----------
1. Google LicenseClassfifer V2 https://github.com/google/licenseclassifier/

2. Ctypes https://docs.python.org/3/library/ctypes.html