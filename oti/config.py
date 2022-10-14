"""The OTI configuration module"""
import dataclasses

DEFAULT_SERVICE_NAME = "UNDEFINED_SERVICE"
DEFAULT_EXPORTER_TYPE = "STDOUT"  # STDOUT | OTELGRPC
DEFAULT_SPAN_PROCESSOR_TYPE = "SIMPLE"  # SIMPLE | BATCH
DEFAULT_OTEL_SAMPLING_TYPE = "NEVER"  # NEVER | PARENTBASED | RATIOBASED | ALWAYS
DEFAULT_OTEL_SAMPLING_RATIO = 1.0
DEFAULT_OTEL_COLLECTOR_URL = "localhost:4317"


@dataclasses.dataclass
class ExporterConfig:
    """The Constructor of exporter configuration class"""

    def __init__(
        self,
        exporter_type=DEFAULT_EXPORTER_TYPE,
        collector_url=DEFAULT_OTEL_COLLECTOR_URL,
    ):
        """The Constructor of exporter configuration class"""
        self.exporter_type = exporter_type
        self.collector_url = collector_url

    def __str__(self):
        """Serialize the object to string"""
        return f'ExporterConfig(exporter_type="{self.exporter_type}", collector_url={self.collector_url})'


@dataclasses.dataclass
class SamplingConfig:
    """The configuration parameters of trace sampling"""

    def __init__(
        self,
        trace_sampling_type=DEFAULT_OTEL_SAMPLING_TYPE,
        trace_sampling_ratio=DEFAULT_OTEL_SAMPLING_RATIO,
    ):
        """The Constructor of trace sampling configuration class"""
        self.trace_sampling_type = trace_sampling_type
        self.trace_sampling_ratio = trace_sampling_ratio

    def __str__(self):
        """Serialize the object to string"""
        return (
            f"SamplingConfig("
            f'trace_sampling_type="{self.trace_sampling_type}", '
            f"trace_sampling_ratio={self.trace_sampling_ratio})"
        )


@dataclasses.dataclass
class OTIConfig:
    """Configuration parameters for Open Telemetry Instrumentation"""

    def __init__(
        self,
        service_name=DEFAULT_SERVICE_NAME,
        span_processor_type=DEFAULT_SPAN_PROCESSOR_TYPE,
        exporter_config=ExporterConfig(),
        sampling_config=SamplingConfig(),
    ):
        """The Constructor of Open Telemetry Instrumentation configuration class"""
        self.service_name = service_name
        self.span_processor_type = span_processor_type
        self.exporter_config = exporter_config
        self.sampling_config = sampling_config

    def __str__(self):
        """Serialize the object to string"""
        return (
            f"OTIConfig("
            f'service_name="{self.service_name}", '
            f'span_processor_type="{self.span_processor_type}", '
            f"exporter_config={self.exporter_config}), "
            f"sampling_config={self.sampling_config})"
        )
