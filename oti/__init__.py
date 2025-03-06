"""
The OTI module

It makes simple to configure and instrument the OTEL SDK for applications that run as standalone processes.
"""

from .oti import OTI
from .config import (
    OTIConfig,
    ExporterConfig,
    SamplingConfig,
    PeriodicMetricReaderConfig,
    MetricReaderEndpointConfig,
)

__all__ = ["oti", "config"]
