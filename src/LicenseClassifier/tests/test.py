from multiprocessing.sharedctypes import Value
import unittest
from pathlib import Path
from LicenseClassifier.classifier import LicenseClassifier
import tempfile
from os import remove


class TestLicenseClassifier(unittest.TestCase):
    # Unittests for LicenseClassifier
    data_location = Path(__file__).parent / "data"

    def test_classifier_init_invalid_threshold(self):
        with self.assertRaises(ValueError):
            LicenseClassifier(0)

        
    def test_classifier_scan_file_format(self):
        test_file = tempfile.mkstemp()[1]
        try:
            l = LicenseClassifier()
            scan_results = l.scan_file(test_file)

            expected = [
                "path",
                "licenses",
                "license_expressions",
                "copyrights",
                "scan_error",
            ]

            self.assertEqual(sorted(expected), sorted(scan_results.keys()))

        finally:
            remove(test_file)

    def test_classifier_scan_file_file_not_found_exception(self):
        l = LicenseClassifier()
        self.assertRaises(FileNotFoundError, l.scan_file, "")

    def test_classifier_scan_file_is_directory_exception(self):
        l = LicenseClassifier()
        scan_results = l.scan_file("/")
        self.assertEqual(scan_results.get("scan_error", None), "read /: is a directory")

    def test_classifier_scan_file_license_info(self):
        l = LicenseClassifier()
        scan_results = l.scan_file(str(self.data_location / "LICENSE"))

        expected = {
            "licenses": [
                {
                    "key": "mit",
                    "score": 1,
                    "start_line": 5,
                    "end_line": 21,
                    "start_index": 0,
                    "end_index": 161,
                    "category": "Permissive",
                }
            ],
            "license_expressions": ["mit"],
        }

        self.assertEqual(len(scan_results.get("licenses", {})), 1)
        self.assertEqual(len(scan_results.get("license_expressions", {})), 1)

        self.assertEqual(expected["licenses"], scan_results.get("licenses", {}))
        self.assertEqual(
            expected["license_expressions"], scan_results.get("license_expressions", {})
        )

    def test_classifier_scan_file_copyright_info(self):
        l = LicenseClassifier()
        scan_results = l.scan_file(str(self.data_location / "LICENSE"))

        expected = {
            "copyrights": [
                {
                    "notification": "Copyright (c) 2021 AvishrantSharma",
                    "start_index": 13,
                    "end_index": 48,
                    "holder": "AvishrantSharma",
                }
            ]
        }

        self.assertEqual(len(scan_results.get("copyrights", {})), 1)

        self.assertEqual(expected["copyrights"], scan_results.get("copyrights", {}))


if __name__ == "__main__":
    unittest.main()
