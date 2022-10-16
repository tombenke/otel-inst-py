examples
========

This directory contains examples for tracing.

## Usage

### Start the observability tools
Some of the examples needs external services e.g. Jaeger, OTEL collector,
so start the [`docker-compose.test.yml`](../docker-compose.test.yml) in the project root folder before using the examples:

```bash
docker-compose -f ../docker-compose.test.yml up
```

### Creates traces that are written to the standard output


Execute the `simple_trace_stdout.py` script:

```bash
python simple_trace_stdout.py 

OTIConfig(service_name="simple_trace_stdout", span_processor_type="SIMPLE", exporter_config=ExporterConfig(exporter_type="STDOUT", collector_url=localhost:4317)), sampling_config=SamplingConfig(trace_sampling_type="ALWAYS", trace_sampling_ratio=1.0))
sampling_type: ALWAYS
TRACER / SPAN is executed: 301428366454877451266075306266720961444
{
    "name": "span-name",
    "context": {
        "trace_id": "0xe2c4fde0558c07774c685a6d2c0b83a4",
        "span_id": "0xa8b670f6503e5663",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": null,
    "start_time": "2022-10-14T14:27:47.564039Z",
    "end_time": "2022-10-14T14:27:47.564075Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {},
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.13.0",
            "service.name": "unknown_service"
        },
        "schema_url": ""
    }
}
```


### Creates traces that are collected with OTEL gRPC protocol

Execute the `simple_trace_otelgrpc.py` script:

```bash
python simple_trace_otelgrpc.py 
OTIConfig(service_name="simple_trace_otelgrpc", span_processor_type="SIMPLE", exporter_config=ExporterConfig(exporter_type="OTELGRPC", collector_url=localhost:4317)), sampling_config=SamplingConfig(trace_sampling_type="ALWAYS", trace_sampling_ratio=1.0))
sampling_type: ALWAYS
TRACER / SPAN is executed: 8be496198edbb3ce99b7271de21b7628
```

Open the Jaeger Web UI on the [http://localhost:16686/](http://localhost:16686/) URL and find the results.
