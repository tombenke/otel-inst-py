"""
This example imports and configures the OTEL SDK via the `OTI` class using environment variables to define the config parameters.

The environment variables are sourced from the `.env_otlpgrpc` file.

The program also imports the OTEL gRPC API to demonstrate the usage of the tracing API.

The results are written to a Trace Collector application using the OTEL gRPC protocol,
so you need to start either the OTEL Collector or Jaeger,
so start the [`docker-compose.test.yml`](../docker-compose.test.yml)
in the project root folder before using this script:

```bash
docker-compose -f ../docker-compose.test.yml up
```
"""
# Load environment variables from .env if exists
import dotenv

dotenv.load_dotenv(".env_otlpgrpc")
# pylint: disable=wrong-import-position
from opentelemetry import trace  # Import the OTEL API
from oti import OTI


# Configure the OTEL SDK
oti = OTI()

# Use the OTEL via API only
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("simple-trace-example") as span:
    # do some work that 'span' will track
    TRACE_ID = str(hex(span.get_span_context().trace_id)[2:])
    print(f"TRACER / SPAN is executed: {TRACE_ID}")
    # When the 'with' block goes out of scope, 'span' is closed for you

# Shut down the OTEL SDK
oti.shutdown()
