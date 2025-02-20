"""
This example uses the tracing API and instruments the OTI with the default config values.
"""

from opentelemetry import trace  # Import the OTEL API
from oti import OTI

# Configure the OTEL SDK
oti = OTI()

# Use the OTEL via API only without the OTI (SDK instrumentation)
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("the-main-span-of-the-example") as span:
    # do some work that 'span' will track
    if span.is_recording():
        span.set_attribute("notes", "This note should appear as a span attribute.")
    print(f"TRACER / SPAN is executed: {span.get_span_context().trace_id}")
    # When the 'with' block goes out of scope, 'span' is closed for you

# Shut down the OTEL SDK
oti.shutdown()
