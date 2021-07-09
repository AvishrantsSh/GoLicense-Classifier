import ctypes
import json
from datetime import datetime, timezone
from os import fsdecode, fsencode, walk
from os.path import dirname, exists, join


class PathIsDir(Exception):
    """Exception raised when given path does not correspond to file"""

    def __str__(self):
        return "The given path does not correspond to a file"


class PathIsFile(Exception):
    """Exception raised when given path does not correspond to a directory"""

    def __str__(self):
        return "The given path does not correspond to a directory"


class InvalidParameter(Exception):
    """Exception raised due to invalid parameters"""

    def __str__(self):
        return "Invalid Paramater"


class LicenseClassifier:
    """
    Base Class
    """

    _ROOT = dirname(__file__)

    # Shared Library
    _so = ctypes.cdll.LoadLibrary(join(_ROOT, "compiled/libmatch.so"))
    _init = _so.CreateClassifier
    _init.argtypes = [ctypes.c_char_p, ctypes.c_double]

    _scanfile = _so.ScanFile
    _scanfile.argtypes = [ctypes.c_char_p]
    _scanfile.restype = ctypes.c_char_p

    def __init__(self, threshold=0.8):
        """
        Initialize LicenseClassifier Object

        Parameters
        ----------
        threshold : float
            Threshold for license scan results. `0 < threshold <= 1.0`
        """

        self._init(
            fsencode(join(LicenseClassifier._ROOT, "classifier/default/")), threshold
        )

    def scan_directory(self, location: str, output: str = "result.json") -> bool:
        """
        Function to find valid license and copyright expressions for files in `location`.

        Parameters
        ----------
        location : str
            Path to location of directory to scan.
        """
        if not exists(location):
            raise FileNotFoundError

        result = []
        start_time = datetime.now(timezone.utc)
        for (dirpath, _, filenames) in walk(location):
            result += [self.scan_file(join(dirpath, file)) for file in filenames]

        end_time = datetime.now(timezone.utc)
        result = {
            "header": [
                {
                    "tool_name": "Golicense-classifier",
                    "input": location,
                    "start_timestamp": start_time.strftime("%Y/%m/%d-%I:%M:%S:%p"),
                    "end_timestamp": end_time.strftime("%Y/%m/%d-%I:%M:%S:%p"),
                    "duration": (end_time - start_time).total_seconds(),
                    "files_count": len(result),
                    # ToDo: Add Error Expressions
                    "errors": [],
                }
            ],
            "files": result,
        }

        return result

    def scan_file(self, location):
        """
        Function to find valid license and copyright expressions in `location`.

        Parameters
        ----------
        location : str
            Path to file.
        """
        # ToDo: DS Marshalling
        # Translation of License Keys

        if not exists(location):
            raise FileNotFoundError

        json_string = fsdecode(self._scanfile(fsencode(location)))

        scan_result = json.loads(json_string)

        # Catch any errors generated during the process
        if scan_result.get("error", None):
            raise ValueError(scan_result["error"])

        return scan_result
