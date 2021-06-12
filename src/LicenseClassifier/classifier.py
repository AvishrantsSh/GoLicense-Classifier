import ctypes
from os import listdir, walk
from os.path import dirname, exists, isdir, isfile, join

from LicenseClassifier.error import PathIsDir, PathIsFile


class LicenseClassifier:
    _ROOT = dirname(__file__)

    # Shared Library
    _so = ctypes.cdll.LoadLibrary(join(_ROOT, "compiled/libmatch.so"))
    _match = _so.FindMatch
    _match.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    _match.restype = ctypes.c_char_p

    _setThresh = _so.SetThreshold
    _setThresh.argtypes = [ctypes.c_int]
    _setThresh.restype = ctypes.c_int

    def __init__(self):
        pass

    def findMatch(self, filepath, output="result.json"):
        """Function to find a license match for file specified by `filepath`"""
        if not exists(filepath):
            raise FileNotFoundError

        if isdir(filepath):
            raise PathIsDir

        res = self._match(
            LicenseClassifier._ROOT.encode("utf-8"),
            filepath.encode("utf-8"),
            output.encode("utf-8"),
        )
        return res.decode("utf-8")

    def catalogueDir(self, root, searchSubDir=True, output="result.json"):
        """Function to find a license match for all files present in `root`"""
        if not exists(root):
            raise FileNotFoundError

        if isfile(root):
            raise PathIsFile

        if searchSubDir:
            filepath = [
                join(dirpath, f)
                for (dirpath, _, filenames) in walk(root)
                for f in filenames
            ]
        else:
            filepath = [join(root, f) for f in listdir(root) if isfile(join(root, f))]

        filepath = "\n".join(filepath)
        res = self._match(
            LicenseClassifier._ROOT.encode("utf-8"),
            filepath.encode("utf-8"),
            output.encode("utf-8"),
        )
        return res.decode("utf-8")

    def setThreshold(self, thresh):
        """Set a threshold between `0 - 100`. Default is `80`. Speed Degrades with lower threshold"""
        _ = self._setThresh(thresh)
