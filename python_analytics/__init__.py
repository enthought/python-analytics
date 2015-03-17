import logging
try:  # pragma: no cover
    from ._version import full_version as __version__
except ImportError:  # pragma: no cover
    __version__ = "not-built"

__all__ = [
    'CustomDimension',
    'CustomMetric',
    'Event',
    'Tracker',
]

from .events import Event
from .event_encoder import CustomDimension, CustomMetric
from .tracker import Tracker


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
