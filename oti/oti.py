"""The OTI class"""

from opentelemetry import trace
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
    OTLPMetricExporter as OTLPMetricExporterHttp,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
    ConsoleMetricExporter,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as OTLPGRPCSpanExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as OTLPHTTPSpanExporter,
)
from opentelemetry.sdk.trace.sampling import (
    ALWAYS_OFF,
    ALWAYS_ON,
    ParentBased,
    TraceIdRatioBased,
)
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server
from .config import OTIConfig


class OTI:
    """
    Class for Open Telemetry Instrumentation

    This is a wrapper for insrtumenting the OTEL SDK for an application.
    It imports the OTEL SDK, and initializes a global tracer.
    It uses the most important configuration parameters, e.g. `service.name`, etc.
    """

    def __init__(self, config=OTIConfig()):
        """Constructor of the Open Telemetry instrumentation object"""

        # Create exporter(s)
        self.config = config
        self.metric_server, self.ms_thread = None, None

        # Create Tracer Provider and set it as global default tracer provider
        self.tracer_provider = self.create_tracer_provider(config)
        trace.set_tracer_provider(self.tracer_provider)

        # Create a Meter Provider and set it as global default meter provider
        self.meter_provider = self.create_meter_provider(config)
        metrics.set_meter_provider(self.meter_provider)

        # Creates a tracer from the global tracer provider
        self.tracer = trace.get_tracer(__name__)

        # Creates a meter from global Meter Provider
        self.meter = metrics.get_meter(__name__)

    def create_tracer_provider(self, config):
        """Setup the global trace provider according to the config parameters"""
        span_exporter = self.setup_span_exporter(config)

        tracer_provider = TracerProvider(
            self.setup_sampler(config.sampling_config),
            resource=Resource.create(
                {
                    "service.name": config.service_name,
                    "service.namespace": config.service_namespace,
                    "service.instance.id": config.service_instance_id,
                    "service.version": config.service_version,
                }
            ),
        )

        tracer_provider.add_span_processor(
            self.setup_span_processor(config, span_exporter)
        )

        return tracer_provider

    def create_meter_provider(self, config):
        """Setup the global meter provider according to the config parameters"""
        readers = []
        reader_periodic = PeriodicExportingMetricReader(
            self.setup_metric_exporter(config),
            export_interval_millis=config.periodic_metric_reader_config.export_interval_millis,
            export_timeout_millis=config.periodic_metric_reader_config.export_timeout_millis,
        )

        reader_endpoint = PrometheusMetricReader()
        if config.metric_exporter_mode_config == "PERIODIC":
            readers = [reader_periodic]
        elif config.metric_exporter_mode_config == "ENDPOINT":
            readers.append(reader_endpoint)
            self.start_metric_server(config)
        elif config.metric_exporter_mode_config == "BOTH":
            readers = [reader_periodic, reader_endpoint]
            self.start_metric_server(config)
        else:
            raise NotImplementedError(
                "Only PERIODIC, ENDPOINT and BOTH modes are supported"
            )

        meter_provider = MeterProvider(
            metric_readers=readers,
            resource=Resource.create(
                {
                    "service.name": config.service_name,
                    "service.namespace": config.service_namespace,
                    "service.instance.id": config.service_instance_id,
                    "service.version": config.service_version,
                }
            ),
        )

        return meter_provider

    def start_metric_server(self, config):
        """Start the metric server. The metrics can be queried via the endpoint specified in the config"""
        endpoint_config = config.metric_exporter_endpoint_config
        self.metric_server, self.ms_thread = start_http_server(
            port=int(endpoint_config.endpoint_port), addr=endpoint_config.endpoint_addr
        )

    def shutdown_metric_server(self):
        """Shut down the metric server"""
        if self.metric_server:
            self.metric_server.shutdown()
            self.ms_thread.join()

    def setup_span_processor(self, config, span_exporter):
        """Setup the trace span processor according to the config parameters"""
        span_processor_type = config.span_processor_type.upper()

        if span_processor_type == "BATCH":
            return BatchSpanProcessor(span_exporter)
        if span_processor_type == "SIMPLE":
            return SimpleSpanProcessor(span_exporter)

        raise OTIConfigError(
            f'Unknown OTEL span processor type: "{config.span_processor_type}"'
        )

    def setup_span_exporter(self, config):
        """Setup the exporter according to the config parameters"""
        exporter_type = config.exporter_config.exporter_type.upper()
        if exporter_type == "STDOUT":
            return ConsoleSpanExporter(service_name=config.service_name)
        if exporter_type == "OTLPGRPC":
            return OTLPGRPCSpanExporter(
                endpoint=config.exporter_config.exporter_url, insecure=True
            )
        if exporter_type == "OTLPHTTP":
            return OTLPHTTPSpanExporter(endpoint=config.exporter_config.exporter_url)

        raise OTIConfigError(
            f'Unknown OTEL span exporter type: "{config.exporter_config.exporter_type}"'
        )

    def setup_metric_exporter(self, config):
        """Setup the exporter according to the config parameters"""
        exporter_type = config.exporter_config.exporter_type.upper()
        if exporter_type == "STDOUT":
            return ConsoleMetricExporter()
        if exporter_type == "OTLPGRPC":
            return OTLPMetricExporter(
                endpoint=config.exporter_config.exporter_url, insecure=True
            )
        if exporter_type == "OTLPHTTP":
            return OTLPMetricExporterHttp(endpoint=config.exporter_config.exporter_url)

        raise OTIConfigError(
            f'Unknown OTEL span exporter type: "{config.exporter_config.exporter_type}"'
        )

    def setup_sampler(self, sampling_config):
        """Setup the trace sampler according to the config parameters"""
        sampling_type = sampling_config.trace_sampling_type.upper()

        if sampling_type == "ALWAYS_OFF":
            # "always_off": AlwaysOffSampler
            return ALWAYS_OFF
        if sampling_type == "ALWAYS_ON":
            # "always_on": AlwaysOnSampler
            return ALWAYS_ON
        if sampling_type == "PARENTBASED_ALWAYS_ON":
            # "parentbased_always_on": ParentBased(root=AlwaysOnSampler)
            return ParentBased(root=ALWAYS_ON)
        if sampling_type == "PARENTBASED_ALWAYS_OFF":
            # "parentbased_always_off": ParentBased(root=AlwaysOffSampler)
            return ParentBased(root=ALWAYS_OFF)
        if sampling_type == "PARENTBASED_TRACEID_RATIO":
            # "parentbased_traceidratio": ParentBased(root=TraceIdRatioBased)
            return ParentBased(
                root=TraceIdRatioBased(sampling_config.trace_sampling_ratio)
            )
        if sampling_type == "TRACEIDRATIO":
            # "traceidratio": TraceIdRatioBased
            return TraceIdRatioBased(sampling_config.trace_sampling_ratio)

        raise OTIConfigError(
            f'Unknown OTEL trace sampling type: "{sampling_config.trace_sampling_type}"'
        )

    def shutdown(self):
        """Shut down the OTEL instrumentation"""
        self.shutdown_metric_server()
        self.tracer_provider.shutdown()
        self.meter_provider.shutdown()


class OTIConfigError(Exception):
    """Inappropriate argument value (of correct type)."""

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass
