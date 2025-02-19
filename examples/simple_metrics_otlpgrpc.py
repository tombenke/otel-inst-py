"""
This example imports and configures the OTEL SDK via the `OTI` class using the `OTIConfig` to define the config parameters.

The program also imports the OTEL gRPC API to demonstrate the usage of the tracing API.

The results are written to a Trace Collector application using the OTEL gRPC protocol,
so you need to start either the OTEL Collector or Jaeger,
so start the [`docker-compose.test.yml`](../docker-compose.test.yml)
in the project root folder before using this script:

```bash
docker-compose -f ../docker-compose.test.yml up
```

After running this small code snippet, check Prometheus for your metrics:
default: localhost:9090
"""

from opentelemetry import metrics

from oti import (
    OTI,
    OTIConfig,
    ExporterConfig,
    SamplingConfig,
    PeriodicMetricReaderConfig,
)


# Configure the OTEL SDK
oti = OTI(
    OTIConfig(
        service_name="simple_metric_otelgrpc",
        service_namespace="examples",
        service_instance_id="stot_42",
        service_version="v1.0.0",
        exporter_config=ExporterConfig(exporter_type="OTLPGRPC"),
        sampling_config=SamplingConfig(trace_sampling_type="PARENTBASED_ALWAYS_ON"),
        metric_exporter_mode_config="PERIODIC",
        periodic_metric_reader_config=PeriodicMetricReaderConfig(1000, 1000),
    )
)

meter = metrics.get_meter(__name__)

# histogram example
http_server_duration = meter.create_histogram(
    name="http.server.duration",
    description="measures the duration of the inbound HTTP request",
    unit="milliseconds",
)

http_server_duration.record(50, {"http.method": "POST", "http.scheme": "https"})
http_server_duration.record(100, {"http.method": "GET", "http.scheme": "https"})


# up-down counter example
customers_in_store = meter.create_up_down_counter(
    name="grocery.customers",
    description="measures the current customers in the grocery store",
)

customers_in_store.add(5, {"account.type": "commercial"})
customers_in_store.add(6, {"account.type": "commercial"})
customers_in_store.add(-2, {"account.type": "commercial"})

# counter example
work_counter = meter.create_counter(
    "work.counter", unit="1", description="Counts the amount of work done"
)


i = 0
while i < 10:
    work_counter.add(1, {"work.type": "example-work"})
    i = i + 1

# Shut down the OTEL SDK
oti.shutdown()
