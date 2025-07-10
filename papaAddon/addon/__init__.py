# Ensure bundled third-party libraries in the "lib" subfolder are importable
import os
import sys

# Addon root folder (the one that contains this __init__.py)
_addon_root: str = os.path.dirname(__file__)
_lib_dir: str = os.path.join(_addon_root, "lib")

# Prepend so that our libs take precedence over any conflicting versions that NVDA might ship.
if _lib_dir not in sys.path:
    sys.path.insert(0, _lib_dir)

# Initialise translation infrastructure as early as possible so that _() works everywhere.
import addonHandler  # noqa: E402 – imported after path manipulation on purpose

addonHandler.initTranslation()