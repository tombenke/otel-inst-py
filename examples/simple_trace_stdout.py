"""
This example imports and configures the OTEL SDK via the `OTI` class using the `OTIConfig` to define the config parameters.

The program also imports the OTEL API to demonstrate the usage of the tracing API.

The results are written to the `stdout`.
"""
from opentelemetry import trace  # Import the OTEL API
from oti import OTI, OTIConfig, ExporterConfig, SamplingConfig

# Configure the OTEL SDK
oti = OTI(
    OTIConfig(
        service_name="simple_trace_stdout",
        service_namespace="examples",
        service_instance_id="st_42",
        service_version="v1.2.3",
        exporter_config=ExporterConfig(exporter_type="STDOUT"),
        sampling_config=SamplingConfig(trace_sampling_type="PARENTBASED_ALWAYS_ON"),
    )
)

# Use the OTEL via API only
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("the-main-span-of-the-example") as span:
    # do some work that 'span' will track
    if span.is_recording():
        span.set_attribute("notes", "This note should appear as a span attribute.")
    print(f"TRACER / SPAN is executed: {span.get_span_context().trace_id}")
    # When the 'with' block goes out of scope, 'span' is closed for you

# Shut down the OTEL SDK
oti.shutdown()
