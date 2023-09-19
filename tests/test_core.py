"""Tests standard tap features using the built-in SDK tests library."""

from singer_sdk.testing import get_tap_test_class
from tap_shapefile.tap import TapShapefile

SAMPLE_CONFIG = {
    "files": [{"entity": "test", "path": "data/test_10", "id": "id"}]
}

TestTapShapefile = get_tap_test_class(
    tap_class = TapShapefile,
    config = SAMPLE_CONFIG,
)