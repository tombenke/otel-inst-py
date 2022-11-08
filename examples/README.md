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

### Use the tracing API without SDK instrumentation

This example demonstrates that it is possible to instrument use OTEL tracing API without using the SDK
The code runs correctly, but the OTEL has no any affect on the execution of the program.
OTEL actually does nothing.

Execute the [simple_trace_stdout_wo_sdk.py](simple_trace_stdout_wo_sdk.py) script:

```bash
python simple_trace_stdout_wo_sdk.py 

TRACER / SPAN is executed: 0
```

### Use the tracing API with the default configuration of the SDK instrumentation

This example uses the tracing API and instruments the OTI with the default config values.

Execute the [simple_trace_stdout_default_config.py](simple_trace_stdout_default_config.py) script:
```bash
python simple_trace_stdout_default_config.py 
TRACER / SPAN is executed: 22333010992527300763747399008028378057
{
    "name": "the-main-span-of-the-example",
    "context": {
        "trace_id": "0x10cd2e7449383bb3f2b4a47ed48ec3c9",
        "span_id": "0x38484677441b4eec",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": null,
    "start_time": "2022-11-08T15:30:42.471515Z",
    "end_time": "2022-11-08T15:30:42.471560Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "notes": "This note should appear as a span attribute."
    },
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.13.0",
            "service.name": "UNDEFINED_SERVICE",
            "service.namespace": "UNDEFINED_SERVICE_NS",
            "service.instance.id": "UNDEFINED_SERVICE_b147e7d0-85ea-42b9-b5be-d03b590724d2",
            "service.version": "UNDEFINED_SERVICE_VERSION"
        },
        "schema_url": ""
    }
}
```

### Create traces that are written to the standard output using OTIConfig object

This example imports and configures the OTEL SDK via the `OTI` class using the `OTIConfig` to define the config parameters.

The program also imports the OTEL API to demonstrate the usage of the tracing API.

The results are written to the `stdout`.

Execute the [`simple_trace_stdout.py`](simple_trace_stdout.py) script:

```bash
python simple_trace_stdout.py 

TRACER / SPAN is executed: 18472302152470526184635391702313846125
{
    "name": "the-main-span-of-the-example",
    "context": {
        "trace_id": "0x0de5a2cff5d12e74d5f1cf699845c56d",
        "span_id": "0xa8c27f290a82095f",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": null,
    "start_time": "2022-11-08T15:17:34.386806Z",
    "end_time": "2022-11-08T15:17:34.386848Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "notes": "This note should appear as a span attribute."
    },
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.13.0",
            "service.name": "simple_trace_stdout",
            "service.namespace": "examples",
            "service.instance.id": "st_42",
            "service.version": "v1.2.3"
        },
        "schema_url": ""
    }
}
```

### Create traces that are written to the standard output using environment variables for OTI configuration

This example imports and configures the OTEL SDK using environment variables to define the config parameters for OTI.

The environment variables are sourced from the [`.env_stdout`](.env_stdout) file:

```bash
export OTEL_SERVICE_NAME=simple_trace_stdout_env
export OTEL_SERVICE_VERSION=v1.2.3
export OTEL_SERVICE_NAMESPACE=examples
```

The program also imports the OTEL API to demonstrate the usage of the tracing API.

The results are written to the `stdout`.

Execute the [`simple_trace_stdout_env.py`](simple_trace_stdout_env.py) script:

```bash
python simple_trace_stdout_env.py 
TRACER / SPAN is executed: 264543772086928889161826432100040226119
{
    "name": "the-main-span-of-the-example",
    "context": {
        "trace_id": "0xc70546f84e226206cd92f9b8b964b547",
        "span_id": "0x331b7e863d66ef0d",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": null,
    "start_time": "2022-11-08T15:36:42.999669Z",
    "end_time": "2022-11-08T15:36:42.999709Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "notes": "This note should appear as a span attribute."
    },
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.13.0",
            "service.name": "simple_trace_stdout_env",
            "service.namespace": "examples",
            "service.instance.id": "simple_trace_stdout_env_5215ffb9-9947-4294-a82d-0e032f9cdc74",
            "service.version": "v1.2.3"
        },
        "schema_url": ""
    }
}
```

### Create traces that are collected with OTEL gRPC protocol using OTIConfig object

This example imports and configures the OTEL SDK via the `OTI` class using the `OTIConfig` to define the config parameters.

The program also imports the OTEL gRPC API to demonstrate the usage of the tracing API.

The results are written to a Trace Collector application using the OTEL gRPC protocol,
so you need to start either the OTEL Collector or Jaeger,
so start the [`docker-compose.test.yml`](../docker-compose.test.yml)
in the project root folder before using this script:

```bash
docker-compose -f ../docker-compose.test.yml up
```

Execute the [`simple_trace_otlpgrpc.py`](simple_trace_otlpgrpc.py) script:

```bash
python simple_trace_otlpgrpc.py 

TRACER / SPAN is executed: 8be496198edbb3ce99b7271de21b7628
```

Open the Jaeger Web UI on the [http://localhost:16686/](http://localhost:16686/) URL and find the results.

### Create traces that are collected with OTEL gRPC protocol using environment variables for OTI configuration

This example imports and configures the OTEL SDK via the `OTI` class using environment variables to define the config parameters.

The environment variables are sourced from the [`.env_otlpgrpc`](.env_otlpgrpc) file:

```bash
export OTEL_SERVICE_NAME=simple_trace_otlpgrpc_env
export OTEL_SERVICE_VERSION=v1.2.3
export OTEL_SERVICE_NAMESPACE=examples
export OTEL_EXPORTER_TYPE=OTLPGRPC
export OTEL_EXPORTER_URL = "http://localhost:4317"
export OTEL_TRACES_SAMPLER=ALWAYS_ON
```

The program also imports the OTEL gRPC API to demonstrate the usage of the tracing API.

The results are written to a Trace Collector application using the OTEL gRPC protocol,
so you need to start either the OTEL Collector or Jaeger,
so start the [`docker-compose.test.yml`](../docker-compose.test.yml)
in the project root folder before using this script:

```bash
docker-compose -f ../docker-compose.test.yml up
```

Execute the [`simple_trace_otlpgrpc_env.py`](simple_trace_otlpgrpc_env.py) script:

```bash
python simple_trace_otlpgrpc_env.py 

TRACER / SPAN is executed: 47e972ef91315092a8b7d6316afaed91
```

Open the Jaeger Web UI on the [http://localhost:16686/](http://localhost:16686/) URL and find the results.


### Create traces that are collected with OTEL HTTP protocol using environment variables for OTI configuration

This example imports and configures the OTEL SDK via the `OTI` class using environment variables to define the config parameters.

The environment variables are sourced from the [`.env_otlphttp`](.env_otlphttp) file:

```bash
export OTEL_SERVICE_NAME=simple_trace_otlphttp_env
export OTEL_SERVICE_VERSION=v1.2.3
export OTEL_SERVICE_NAMESPACE=examples
export OTEL_EXPORTER_TYPE=OTLPHTTP
export OTEL_EXPORTER_URL = "http://localhost:4318/v1/traces"
export OTEL_TRACES_SAMPLER=ALWAYS_ON
```

The program also imports the OTEL HTTP API to demonstrate the usage of the tracing API.

The results are written to a Trace Collector application using the OTEL gRPC protocol,
so you need to start either the OTEL Collector or Jaeger,
so start the [`docker-compose.test.yml`](../docker-compose.test.yml)
in the project root folder before using this script:

```bash
docker-compose -f ../docker-compose.test.yml up
```

Execute the [`simple_trace_otlphttp_env.py`](simple_trace_otlphttp_env.py) script:

```bash
python simple_trace_otlphttp_env.py 

TRACER / SPAN is executed: 3da8518ee7bf5eb8e71f0ac6b7c160a
```

Open the Jaeger Web UI on the [http://localhost:16686/](http://localhost:16686/) URL and find the results.
