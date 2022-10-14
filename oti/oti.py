"""The OTI class"""
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.sampling import (
    ALWAYS_OFF,
    ALWAYS_ON,
    ParentBased,
    TraceIdRatioBased,
)
from .config import OTIConfig


class OTI:
    """
    Class for Open Telemetry Instrumentation
    """

    def __init__(self, config=OTIConfig()):
        """Constructor of the Open Telemetry instrumentation object"""

        print(config)
        # Create exporter(s)
        span_exporter = self.setup_exporter(config)

        # Create a global Tracer Provider
        self.setup_global_tracer_provider(config, span_exporter)

        # Creates a tracer from the global tracer provider
        self.tracer = trace.get_tracer(__name__)

        # Create a global Meter Provider
        # TO DO

        # Create global Propagator
        # TO DO

    def setup_global_tracer_provider(self, config, span_exporter):
        """Setup the global trace provider according to the config parameters"""
        self.tracer_provider = TracerProvider(
            self.setup_sampler(config.sampling_config)
        )

        self.tracer_provider.add_span_processor(
            self.setup_span_processor(config, span_exporter)
        )

        # Sets the global default tracer provider
        trace.set_tracer_provider(self.tracer_provider)

    def setup_span_processor(self, config, span_exporter):
        """Setup the trace span processor according to the config parameters"""
        span_processor_type = config.span_processor_type.upper()

        if span_processor_type == "BATCH":
            return BatchSpanProcessor(span_exporter)
        if span_processor_type == "SIMPLE":
            return SimpleSpanProcessor(span_exporter)

        raise Exception(
            f'Unknown OTEL span processor type: "{config.span_processor_type}"'
        )

    def setup_exporter(self, config):
        """Setup the exporter according to the config parameters"""
        exporter_type = config.exporter_config.exporter_type.upper()
        if exporter_type == "STDOUT":
            return ConsoleSpanExporter(service_name=config.service_name)
        if exporter_type == "OTELGRPC":
            return OTLPSpanExporter()

        raise Exception(
            f'Unknown OTEL span exporter type: "{config.exporter_config.exporter_type}"'
        )

    def setup_sampler(self, sampling_config):
        """Setup the trace sampler according to the config parameters"""
        sampling_type = sampling_config.trace_sampling_type.upper()

        print(f"sampling_type: {sampling_type}")
        if sampling_type == "NEVER":
            return ALWAYS_OFF
        if sampling_type == "ALWAYS":
            return ALWAYS_ON
        if sampling_type == "PARENTBASED":
            return ParentBased(None)
        if sampling_type == "RATIOBASED":
            return TraceIdRatioBased(sampling_config.trace_sampling_ratio)

        raise Exception(
            f'Unknown OTEL trace sampling type: "{sampling_config.trace_sampling_type}"'
        )

    def shutdown(self):
        """Shut down the OTEL instrumentation"""
        self.tracer_provider.shutdown()
