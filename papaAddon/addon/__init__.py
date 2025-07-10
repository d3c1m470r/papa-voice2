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

from importlib import import_module

# Expose sub-modules so that absolute imports like `papaVoiceReader.extract_content`
# succeed when this add-on is installed under NVDA.
# When NVDA loads the add-on it places the add-on directory (named after the
# add-on identifier, i.e. ``papaVoiceReader``) on ``sys.path``.  Because this
# directory also contains our Python package with the same name, we need to
# ensure that importing ``papaVoiceReader`` yields the inner package rather than
# the outer directory itself.  We therefore import the inner package here and
# re-export it so ``sys.modules['papaVoiceReader']`` resolves correctly.

_inner_pkg = import_module('.papaVoiceReader', __package__)
sys.modules[__name__] = _inner_pkg

# Clean-up namespace
del import_module, sys, _inner_pkg