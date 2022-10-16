"""
This example uses the `OTIConfig` with default values.

The program uses the tracing API, but there is no trace exported to gRPC
neither to `stdout` because the corresponding default config values are:

```bash
DEFAULT_EXPORTER_TYPE = "STDOUT"
DEFAULT_OTEL_SAMPLING_TYPE = "NEVER"
```

"""
from opentelemetry import trace  # Import the OTEL API
from oti import OTI, OTIConfig, ExporterConfig, SamplingConfig

# Configure the OTEL SDK
oti = OTI()

# Use the OTEL via API only
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("the-main-span-of-the-example") as span:
    # do some work that 'span' will track
    if span.is_recording():
        span.set_attribute("notes", "This note never should appear!")
    print(f"TRACER / SPAN is executed: {span.get_span_context().trace_id}")
    # When the 'with' block goes out of scope, 'span' is closed for you

# Shut down the OTEL SDK
oti.shutdown()
