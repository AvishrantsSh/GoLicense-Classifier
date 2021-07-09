import ctypes, time
from os import walk
from os.path import dirname, exists, join
import json

from LicenseClassifier.error import *


class LicenseClassifier:
    _ROOT = dirname(__file__)

    # Shared Library
    _so = ctypes.cdll.LoadLibrary(join(_ROOT, "compiled/libmatch.so"))
    _init = _so.CreateClassifier
    _init.argtypes = [ctypes.c_char_p]

    _match = _so.FindMatch
    _match.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    _match.restype = ctypes.c_bool

    _scanfile = _so.ScanFile
    _scanfile.argtypes = [ctypes.c_char_p]
    _scanfile.restype = ctypes.c_char_p

    _setThresh = _so.SetThreshold
    _setThresh.argtypes = [ctypes.c_int]
    _setThresh.restype = ctypes.c_bool

    def __init__(self):
        self._init(join(LicenseClassifier._ROOT, "classifier/default/").encode("utf-8"))
        pass

    def analyze(self, root: str, threading: bool =True, output: str="result.json", maxRoutines=10) -> bool:
        """
        Function to find valid license and copyright expressions for all files present in `root`.
        
        Parameters
        ----------
        root : str
            Path to root of directory to scan.
        threading : bool
            Use threading during scan. May consume significantly more memory and CPU.
        output : str
            Output path for JSON file. Default is `result.json`
        maxRoutines : int
            Maximum number of routines/threads to run concurrently.
        """
        if not exists(root):
            raise FileNotFoundError

        if threading:
            if maxRoutines < 0:
                raise InvalidParameter

            res = self._match(
                root.encode("utf-8"),
                output.encode("utf-8"),
                maxRoutines,
            )
            return res

        else:
            result = []
            start_time = time.time()
            for (dirpath, _, filenames) in walk(root):
                result += [self.scanFile(join(dirpath, file)) for file in filenames]

            end_time = time.time()
            result = {
                "header": [
                    {
                        "tool_name": "Golicense_classifier",
                        "input": root,
                        "start_timestamp": start_time,
                        "end_timestamp": end_time,
                        "duration": end_time - start_time,
                        "files_count": len(result),
                        # ToDo: Add Error Expressions
                        "errors": [],
                    }
                ],
                "files": result,
            }
            
            out_file = open(output, "w")
            json.dump(result, out_file, indent=4)

    def scanFile(self, root):
        """
        Function to find valid license and copyright expressions in `root`.
        
        Parameters
        ----------
        root : str
            Path to file.
        """
        if not exists(root):
            raise FileNotFoundError

        jsonRes = self._scanfile(root.encode("utf-8")).decode('utf-8')

        # Catch any errors generated during making scan results
        if jsonRes[:5] == "Error":
            raise ValueError(jsonRes[6:])

        return json.loads(jsonRes)

    def setThreshold(self, thresh):
        """Set a threshold between `0 - 100`. Default is `80`. Speed Degrades with lower threshold"""
        _ = self._setThresh(thresh)
