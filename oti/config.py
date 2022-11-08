"""The OTI configuration class"""
import dataclasses
import uuid
import os

DEFAULT_SERVICE_NAME = "UNDEFINED_SERVICE"
DEFAULT_SERVICE_NAMESPACE = "UNDEFINED_SERVICE_NS"
DEFAULT_SERVICE_VERSION = "UNDEFINED_SERVICE_VERSION"
DEFAULT_OTEL_EXPORTER_TYPE = "STDOUT"  # STDOUT | OTLPGRPC | OTLPHTTP
DEFAULT_OTEL_EXPORTER_URL = "http://localhost:4317"  # "http://localhost:4318/v1/traces"
DEFAULT_SPAN_PROCESSOR_TYPE = "SIMPLE"  # SIMPLE | BATCH
# ALWAYS_OFF | ALWAYS_ON | TRACEIDRATIO | PARENTBASED | PARENTBASED_ALWAYS_OFF | PARENTBASED_ALWAYS_ON | PARENTBASED_TRACEIDRATIO
DEFAULT_OTEL_SAMPLING_TYPE = "PARENTBASED_ALWAYS_ON"
DEFAULT_OTEL_SAMPLING_RATIO = "1.0"


@dataclasses.dataclass
class ExporterConfig:
    """The Constructor of exporter configuration class"""

    exporter_type: str
    exporter_url: str

    def __init__(
        self,
        exporter_type=None,
        exporter_url=None,
    ):
        """The Constructor of exporter configuration class"""
        self.exporter_type = get_init_value(
            exporter_type, DEFAULT_OTEL_EXPORTER_TYPE, "OTEL_EXPORTER_TYPE"
        )
        self.exporter_url = get_init_value(
            exporter_url, DEFAULT_OTEL_EXPORTER_URL, "OTEL_EXPORTER_URL"
        )

    def __str__(self):
        """Serialize the object to string"""
        return f'ExporterConfig(exporter_type="{self.exporter_type}", exporter_url={self.exporter_url})'


@dataclasses.dataclass
class SamplingConfig:
    """The configuration parameters of trace sampling"""

    def __init__(
        self,
        trace_sampling_type=None,
        trace_sampling_ratio=None,
    ):
        """The Constructor of trace sampling configuration class"""
        self.trace_sampling_type = get_init_value(
            trace_sampling_type, DEFAULT_OTEL_SAMPLING_TYPE, "OTEL_TRACES_SAMPLER"
        )
        self.trace_sampling_ratio = float(
            get_init_value(
                trace_sampling_ratio,
                DEFAULT_OTEL_SAMPLING_RATIO,
                "OTEL_TRACES_SAMPLER_ARG",
            )
        )

    def __str__(self):
        """Serialize the object to string"""
        return (
            f"SamplingConfig("
            f'trace_sampling_type="{self.trace_sampling_type}", '
            f"trace_sampling_ratio={self.trace_sampling_ratio})"
        )


def get_init_value(param_value, default_value, env_var_name=None):
    """
    Get the initial value of a config parameter.
    If there is an environment variable set for this parameter, then uses that value, if not, it returns the default value.
    """
    if param_value is not None:
        return param_value
    if env_var_name is not None:
        return os.environ.get(env_var_name, default_value)
    return default_value


@dataclasses.dataclass
class OTIConfig:
    """
    Configuration parameters for Open Telemetry Instrumentation

    This class holds those configuration parameters that are most frequently used for instrumenting the OTEL SDK.
    """

    def __init__(
        self,
        service_name=None,
        service_namespace=None,
        service_instance_id=None,
        service_version=None,
        span_processor_type=None,
        exporter_config=None,
        sampling_config=None,
    ):
        """The Constructor of Open Telemetry Instrumentation configuration class"""
        self.service_name = get_init_value(
            service_name, DEFAULT_SERVICE_NAME, "OTEL_SERVICE_NAME"
        )
        self.service_namespace = get_init_value(
            service_namespace, DEFAULT_SERVICE_NAMESPACE, "OTEL_SERVICE_NAMESPACE"
        )
        if service_instance_id is not None:
            self.service_instance_id = service_instance_id
        else:
            self.service_instance_id = f"{self.service_name}_{str(uuid.uuid4())}"
        self.service_version = get_init_value(
            service_version, DEFAULT_SERVICE_VERSION, "OTEL_SERVICE_VERSION"
        )
        self.span_processor_type = get_init_value(
            span_processor_type, DEFAULT_SPAN_PROCESSOR_TYPE, "OTEL_SPAN_PROCESSOR_TYPE"
        )

        self.sampling_config = SamplingConfig()
        if sampling_config is not None:
            self.sampling_config = sampling_config

        self.exporter_config = ExporterConfig()
        if exporter_config is not None:
            self.exporter_config = exporter_config

    def __str__(self):
        """Serialize the object to string"""
        return (
            f"OTIConfig("
            f'service_name="{self.service_name}", '
            f'span_processor_type="{self.span_processor_type}", '
            f"exporter_config={self.exporter_config}), "
            f"sampling_config={self.sampling_config})"
        )
