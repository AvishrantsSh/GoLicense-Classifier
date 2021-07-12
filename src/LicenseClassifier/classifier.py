import ctypes
import json
import os
from datetime import datetime, timezone


class LicenseClassifier:
    """
    Base Class
    """

    _ROOT = os.path.dirname(__file__)

    # Shared Library
    _so = ctypes.cdll.LoadLibrary(os.path.join(_ROOT, "compiled/libmatch.so"))
    _init = _so.CreateClassifier
    _init.argtypes = [ctypes.c_char_p, ctypes.c_double]

    _scanfile = _so.ScanFile
    _scanfile.argtypes = [ctypes.c_char_p]
    _scanfile.restype = ctypes.c_char_p

    def __init__(self, threshold: float = 0.8) -> None:
        """
        Initialize LicenseClassifier Object

        Parameters
        ----------
        threshold : float
            Threshold for license scan results. `0 < threshold <= 1.0`
        """
        if not 0 < threshold <= 1:
            raise ValueError("Threshold out of bounds (0 < threshold <= 1)")

        self._init(
            os.fsencode(os.path.join(LicenseClassifier._ROOT, "licenses/")), threshold
        )

    def scan_directory(self, location: str):
        """
        Function to find valid license and copyright expressions for files in `location`.

        Parameters
        ----------
        location : str
            Path to location of directory to scan.
        """
        if not os.path.exists(location):
            raise FileNotFoundError

        result = []
        start_time = datetime.now(timezone.utc)
        for (dirpath, _, filenames) in os.walk(location):
            result += [
                self.scan_file(os.path.join(dirpath, file)) for file in filenames
            ]

        result = sorted(result, key=lambda k: k["path"])
        end_time = datetime.now(timezone.utc)
        scan_result = {
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

        return scan_result

    def scan_file(self, location: str):
        """
        Function to find valid license and copyright expressions in `location`.

        Parameters
        ----------
        location : str
            Path to file.
        """
        # ToDo: DS Marshalling

        if not os.path.exists(location):
            raise FileNotFoundError

        json_string = os.fsdecode(self._scanfile(os.fsencode(location)))

        scan_result = json.loads(json_string)

        # Catch any errors generated during the process
        if scan_result.get("error", None):
            raise ValueError(scan_result["error"])

        # Update license key with scancode.io mapping
        for i in range(len(scan_result["licenses"])):
            mapping = license_classifier_to_scancode_mapping[
                scan_result["licenses"][i]["key"]
            ]
            scan_result["licenses"][i]["key"] = mapping[0]
            scan_result["licenses"][i]["category"] = mapping[1]
            scan_result["license_expressions"][i] = mapping[0]

        return scan_result


# Translation of License Keys
license_classifier_to_scancode_mapping = {
    "0BSD": ["bsd-zero", "Permissive"],
    "AFL-1.1": ["afl-1.1", "Permissive"],
    "AFL-1.2": ["afl-1.2", "Permissive"],
    "AFL-2.0": ["afl-2.0", "Permissive"],
    "AFL-2.1": ["afl-2.1", "Permissive"],
    "AFL-3.0": ["afl-3.0", "Permissive"],
    "AGPL-1.0": ["agpl-1.0", "Copyleft"],
    "AGPL-3.0": ["agpl-3.0", "Copyleft"],
    "AML": ["aml", "Permissive"],
    "AMPAS": ["ampas", "Permissive"],
    "APSL-1.0": ["apsl-1.0", "Copyleft Limited"],
    "APSL-1.1": ["apsl-1.1", "Copyleft Limited"],
    "APSL-1.2": ["apsl-1.2", "Copyleft Limited"],
    "APSL-2.0": ["apsl-2.0", "Copyleft Limited"],
    "Apache-1.0": ["apache-1.0", "Permissive"],
    "Apache-1.1": ["apache-1.1", "Permissive"],
    "Apache-2.0": ["apache-2.0", "Permissive"],
    "Artistic-1.0-Perl": ["artistic-perl-1.0", "Copyleft Limited"],
    "Artistic-1.0-cl8": ["artistic-1.0-cl8", "Copyleft Limited"],
    "Artistic-1.0": ["artistic-1.0", "Copyleft Limited"],
    "Artistic-2.0": ["artistic-2.0", "Copyleft Limited"],
    "Atmel": ["bsd-new", "Permissive"],
    "BCL": ["oracle-bcl-javase-platform-javafx-2013", "Proprietary Free"],
    "BSD-2-Clause-FreeBSD": ["bsd-2-clause-views", "Permissive"],
    "BSD-2-Clause-NetBSD": ["bsd-simplified", "Permissive"],
    "BSD-2-Clause": ["bsd-simplified", "Permissive"],
    "BSD-3-Clause-Attribution": ["bsd-ack", "Permissive"],
    "BSD-3-Clause-Clear": ["clear-bsd", "Permissive"],
    "BSD-3-Clause-LBNL": ["lbnl-bsd", "Permissive"],
    "BSD-3-Clause": ["bsd-3-clause-sun", "Permissive"],
    "BSD-4-Clause-UC": ["bsd-original-uc", "Permissive"],
    "BSD-4-Clause": ["bsd-original", "Permissive"],
    "BSD-Protection": ["bsd-protection", "Copyleft"],
    "BSL-1.0": ["boost-1.0", "Permissive"],
    "BabelstoneIDS": ["BabelstoneIDS", ""],
    "Beerware": ["beerware", "Permissive"],
    "BitTorrent-1.1": ["bittorrent-1.1", "Copyleft Limited"],
    "Business-Source-License-1.1": ["bsl-1.1", "Source-available"],
    "CC-BY-1.0": ["cc-by-1.0", "Permissive"],
    "CC-BY-2.0": ["cc-by-2.0", "Permissive"],
    "CC-BY-2.5": ["cc-by-2.5", "Permissive"],
    "CC-BY-3.0": ["cc-by-3.0", "Permissive"],
    "CC-BY-4.0": ["cc-by-4.0", "Permissive"],
    "CC-BY-NC-1.0": ["cc-by-nc-1.0", "Source-available"],
    "CC-BY-NC-2.0": ["cc-by-nc-2.0", "Source-available"],
    "CC-BY-NC-2.5": ["cc-by-nc-2.5", "Source-available"],
    "CC-BY-NC-3.0": ["cc-by-nc-3.0", "Source-available"],
    "CC-BY-NC-4.0": ["cc-by-nc-4.0", "Source-available"],
    "CC-BY-NC-ND-1.0": ["cc-by-nc-nd-1.0", "Source-available"],
    "CC-BY-NC-ND-2.0": ["cc-by-nc-nd-2.0", "Source-available"],
    "CC-BY-NC-ND-2.5": ["cc-by-nc-nd-2.5", "Source-available"],
    "CC-BY-NC-ND-3.0": ["cc-by-nc-nd-3.0", "Source-available"],
    "CC-BY-NC-ND-4.0": ["cc-by-nc-nd-4.0", "Source-available"],
    "CC-BY-NC-SA-1.0": ["cc-by-nc-sa-1.0", "Source-available"],
    "CC-BY-NC-SA-2.0": ["cc-by-nc-sa-2.0", "Source-available"],
    "CC-BY-NC-SA-2.5": ["cc-by-nc-sa-2.5", "Source-available"],
    "CC-BY-NC-SA-3.0": ["cc-by-nc-sa-3.0", "Source-available"],
    "CC-BY-NC-SA-4.0": ["cc-by-nc-sa-4.0", "Source-available"],
    "CC-BY-ND-1.0": ["cc-by-nd-1.0", "Source-available"],
    "CC-BY-ND-2.0": ["cc-by-nd-2.0", "Source-available"],
    "CC-BY-ND-2.5": ["cc-by-nd-2.5", "Source-available"],
    "CC-BY-ND-3.0": ["cc-by-nd-3.0", "Source-available"],
    "CC-BY-ND-4.0": ["cc-by-nd-4.0", "Source-available"],
    "CC-BY-SA-1.0": ["cc-by-sa-1.0", "Permissive"],
    "CC-BY-SA-2.0": ["cc-by-sa-2.0", "Copyleft Limited"],
    "CC-BY-SA-2.5": ["cc-by-sa-2.5", "Copyleft Limited"],
    "CC-BY-SA-3.0": ["cc-by-sa-3.0", "Copyleft Limited"],
    "CC-BY-SA-4.0": ["cc-by-sa-4.0", "Copyleft"],
    "CC0-1.0": ["cc0-1.0", "Public Domain"],
    "CDDL-1.0": ["cddl-1.0", "Copyleft Limited"],
    "CDDL-1.1": ["cddl-1.1", "Copyleft Limited"],
    "CPAL-1.0": ["cpal-1.0", "Copyleft"],
    "CPL-1.0": ["cpl-1.0", "Copyleft Limited"],
    "Commons-Clause": ["commons-clause", "Source-available"],
    "DBAD": ["dbad-1.1", "Permissive"],
    "EPL-1.0": ["epl-1.0", "Copyleft Limited"],
    "EPL-2.0": ["epl-2.0", "Copyleft Limited"],
    "EUPL-1.0": ["eupl-1.0", "Copyleft"],
    "EUPL-1.1": ["eupl-1.1", "Copyleft Limited"],
    "FTL": ["freetype", "Permissive"],
    "Facebook-2-Clause": ["facebook-nuclide", "Proprietary Free"],
    "Facebook-3-Clause": ["facebook-nuclide", "Proprietary Free"],
    "Facebook-Examples": ["proprietary-license", "Commercial"],
    "FreeImage": ["freeimage-1.0", "Copyleft Limited"],
    "GPL-1.0": ["gpl-1.0", "Copyleft"],
    "GPL-2.0-with-GCC-exception": ["gpl-2.0", "Copyleft"],
    "GPL-2.0-with-autoconf-exception": ["gpl-2.0", "Copyleft"],
    "GPL-2.0-with-bison-exception": ["gpl-2.0", "Copyleft"],
    "GPL-2.0-with-classpath-exception": ["gpl-2.0", "Copyleft"],
    "GPL-2.0-with-font-exception": ["gpl-2.0", "Copyleft"],
    "GPL-2.0": ["gpl-2.0", "Copyleft"],
    "GPL-3.0-with-GCC-exception": ["gpl-3.0", "Copyleft"],
    "GPL-3.0-with-autoconf-exception": ["gpl-3.0", "Copyleft"],
    "GPL-3.0-with-bison-exception": ["gpl-3.0-plus", "Copyleft"],
    "GPL-3.0": ["gpl-3.0", "Copyleft"],
    "GUST-Font-License": ["gust-font-1.0", "Copyleft"],
    "IPL-1.0": ["ibmpl-1.0", "Copyleft Limited"],
    "ISC": ["isc", "Permissive"],
    "ImageMagick": ["apache-2.0", "Permissive"],
    "JSON": ["json", "Permissive"],
    "LGPL-2.0": ["lgpl-2.0", "Copyleft Limited"],
    "LGPL-2.1": ["lgpl-2.1", "Copyleft Limited"],
    "LGPL-3.0": ["lgpl-3.0", "Copyleft Limited"],
    "LGPLLR": ["lgpllr", "Copyleft Limited"],
    "LPL-1.0": ["lucent-pl-1.0", "Copyleft Limited"],
    "LPL-1.02": ["lucent-pl-1.02", "Copyleft Limited"],
    "LPPL-1.3c": ["lppl-1.3c", "Copyleft"],
    "Libpng": ["libpng", "Permissive"],
    "Lil-1.0": ["lil-1", "Permissive"],
    "Linux-OpenIB": ["linux-openib", "Permissive"],
    "MIT": ["mit", "Permissive"],
    "MPL-1.0": ["mpl-1.0", "Copyleft Limited"],
    "MPL-1.1": ["mpl-1.1", "Copyleft Limited"],
    "MPL-2.0-no-copyleft-exception": [
        "mpl-2.0-no-copyleft-exception",
        "Copyleft Limited",
    ],
    "MPL-2.0": ["mpl-2.0", "Copyleft Limited"],
    "MS-PL": ["ms-pl", "Permissive"],
    "MS-RL": ["ms-rl", "Copyleft Limited"],
    "NCBI": ["public-domain", "Public Domain"],
    "NCSA": ["uoi-ncsa", "Permissive"],
    "NPL-1.0": ["npl-1.0", "Copyleft Limited"],
    "NPL-1.1": ["npl-1.1", "Copyleft Limited"],
    "OFL-1.1": ["ofl-1.1", "Permissive"],
    "OSL-1.0": ["osl-1.0", "Copyleft"],
    "OSL-1.1": ["osl-1.1", "Copyleft"],
    "OSL-2.0": ["osl-2.0", "Copyleft"],
    "OSL-2.1": ["osl-2.1", "Copyleft"],
    "OSL-3.0": ["osl-3.0", "Copyleft"],
    "OpenSSL": ["openssl-ssleay", "Permissive"],
    "OpenVision": ["other-permissive", "Permissive"],
    "PHP-3.0": ["php-3.0", "Permissive"],
    "PHP-3.01": ["php-3.01", "Permissive"],
    "PIL": ["secret-labs-2011", "Permissive"],
    "PostgreSQL": ["postgresql", "Permissive"],
    "Python-2.0-complete": ["python", "Permissive"],
    "Python-2.0": ["psf-2.0", "Permissive"],
    "QPL-1.0": ["qpl-1.0", "Copyleft Limited"],
    "Ruby": ["ruby", "Copyleft Limited"],
    "SGI-B-1.0": ["sgi-fslb-1.0", "Free Restricted"],
    "SGI-B-1.1": ["sgi-freeb-1.1", "Permissive"],
    "SGI-B-2.0": ["sgi-freeb-2.0", "Permissive"],
    "SISSL-1.2": ["sun-sissl-1.2", "Proprietary Free"],
    "SISSL": ["sun-sissl-1.1", "Proprietary Free"],
    "Sleepycat": ["sleepycat", "Copyleft"],
    "UPL-1.0": ["upl-1.0", "Permissive"],
    "Unicode-DFS-2015": ["unicode-dfs-2015", "Permissive"],
    "Unicode-DFS-2016": ["unicode-dfs-2016", "Permissive"],
    "Unicode-TOU": ["unicode-tou", "Proprietary Free"],
    "Unlicense": ["unlicense", "Public Domain"],
    "W3C-19980720": ["w3c-software-19980720", "Permissive"],
    "W3C-20150513": ["w3c-software-doc-20150513", "Permissive"],
    "W3C": ["w3c", "Permissive"],
    "WTFPL": ["wtfpl-2.0", "Public Domain"],
    "X11": ["x11-xconsortium", "Permissive"],
    "Xnet": ["xnet", "Permissive"],
    "ZPL-1.1": ["zpl-1.1", "Permissive"],
    "ZPL-2.0": ["zpl-2.0", "Permissive"],
    "ZPL-2.1": ["zpl-2.1", "Permissive"],
    "Zend-2.0": ["zend-2.0", "Permissive"],
    "Zlib": ["zlib", "Permissive"],
    "blessing": ["blessing", "Public Domain"],
    "bzip2-1.0.3": ["bzip2-libbzip-2010", "Permissive"],
    "bzip2-1.0.4": ["bzip2-libbzip-2010", "Permissive"],
    "bzip2-1.0.5": ["bzip2-libbzip-2010", "Permissive"],
    "bzip2-1.0.6": ["bzip2-libbzip-2010", "Permissive"],
    "bzip2-1.0": ["bzip2-libbzip-2010", "Permissive"],
    "eGenix": ["egenix-1.1.0", "Permissive"],
    "libtiff": ["x11-tiff", "Permissive"],
    "zlib-acknowledgement": ["zlib-acknowledgement", "Permissive"],
}
