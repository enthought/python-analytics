import logging
try:  # pragma: no cover
    from ._version import full_version as __version__
except ImportError:  # pragma: no cover
    __version__ = "not-built"


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
