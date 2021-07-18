# Golicense-Classifier
A Python based module to find valid copyright and license expressions in a file.

_Note: This module is based on Google LicenseClassifier._

## Installation
Currently, this package only supports Linux Platform. Work is in progress for Windows and Mac.

To install from Pypi, use
```sh
pip install golicense-classifier
```

## Usage
To get started, import `LicenseClassifier` class from the module as

```python
from LicenseClassifier.classifier import LicenseClassifier
```

_Note: Work on Copyright Statement is still in progress. Expect some issues, mostly with binary files_

The class comes bundled with several functions for scanning purpose.

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
        
        `(Experimental)` Set `True` to use buffered file scanning. `max_size` will be used as buffer size.


2. `scan_file`

    This method is used to find license expressions and copyright statements on a single file.
    
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
        
        `(Experimental)` Set `True` to use buffered file scanning. `max_size` will be used as buffer size.

## Setting Custom Scanning Threshold

You can set custom threshold for scanning purpose that best suits your need. For this, you can use parameter `threshold` while making object as
```python
classifier = LicenseClassifier(threshold = 0.9)
```