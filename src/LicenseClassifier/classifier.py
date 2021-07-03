import ctypes
from os.path import dirname, exists, join

from LicenseClassifier.error import *


class LicenseClassifier:
    _ROOT = dirname(__file__)

    # Shared Library
    _so = ctypes.cdll.LoadLibrary(join(_ROOT, "compiled/libmatch.so"))
    _match = _so.FindMatch
    _match.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    _match.restype = ctypes.c_bool

    _setThresh = _so.SetThreshold
    _setThresh.argtypes = [ctypes.c_int]
    _setThresh.restype = ctypes.c_bool

    def __init__(self):
        pass

    def analyze(self, root, searchSubDir=True, output="result.json"):
        """Function to find a license match for all files present in `root`"""
        if not exists(root):
            raise FileNotFoundError

        res = self._match(
            LicenseClassifier._ROOT.encode("utf-8"),
            root.encode("utf-8"),
            output.encode("utf-8"),
        )
        return res

    def setThreshold(self, thresh):
        """Set a threshold between `0 - 100`. Default is `80`. Speed Degrades with lower threshold"""
        _ = self._setThresh(thresh)
