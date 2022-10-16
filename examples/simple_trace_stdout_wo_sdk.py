"""
This example demonstrates that it is possible to instrument use OTEL tracing API without using the SDK
The code runs correctly, but the OTEL has no any affect on the execution of the program.
OTEL actually does nothing.
"""
from opentelemetry import trace  # Import the OTEL API

# Use the OTEL via API only
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("the-main-span-of-the-example") as span:
    # do some work that 'span' will track
    print(f"TRACER / SPAN is executed: {span.get_span_context().trace_id}")
    # When the 'with' block goes out of scope, 'span' is closed for you
