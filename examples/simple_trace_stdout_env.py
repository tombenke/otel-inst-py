"""
This example imports and configures the OTEL SDK using environment variables to define the config parameters for OTI.

The environment variables are sourced from the `.env_stdout` file.

The program also imports the OTEL API to demonstrate the usage of the tracing API.

The results are written to the `stdout`.
"""
# Load environment variables from .env if exists
import dotenv

dotenv.load_dotenv(".env_stdout")

# pylint: disable=wrong-import-position
from opentelemetry import trace  # Import the OTEL API
from oti import OTI

# Configure the OTEL SDK
oti = OTI()

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
