otel-inst-py
============

[![Quality Check Status](https://github.com/tombenke/otel-inst-py/workflows/Quality%20Check/badge.svg)](https://github.com/tombenke/otel-inst-py)
[![Release Status](https://github.com/tombenke/otel-inst-py/workflows/Release/badge.svg)](https://github.com/tombenke/otel-inst-py)
![Coverage](./coverage.svg)

## About

Python package that provides the basic features required for Open-Telemetry instrumentation.
It makes easier the manual instrumentation of a python application.

## Usage

### Installation

Install the [`otel-inst-py`](https://pypi.org/project/otel-inst-py/) package with pip, or add it to the requirements.txt or setup.py of your program.

### Configuration

Instantiate the `OTI()` class either with the `OTIConfig()` configuration or via environment variables.

The following code shows the instrumentation using the config objects:

```python
from opentelemetry import trace, metrics  # Import the OTEL API
from oti import OTI, OTIConfig, ExporterConfig, SamplingConfig, PeriodicMetricReaderConfig

# Configure the OTEL SDK
oti = OTI(
    OTIConfig(
        service_name="simple_trace_otelgrpc",
        service_namespace="examples",
        service_instance_id="stot_42",
        service_version="v1.0.0",
        exporter_config=ExporterConfig(exporter_type="OTLPGRPC"),
        sampling_config=SamplingConfig(trace_sampling_type="PARENTBASED_ALWAYS_ON"),
        metric_exporter_mode_config="PERIODIC",
        periodic_metric_reader_config=PeriodicMetricReaderConfig(1000),
    )
)

# Use the OTEL via API only
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("simple-trace-example") as span:
    # do some work that 'span' will track
    TRACE_ID = str(hex(span.get_span_context().trace_id)[2:])
    print(f"TRACER / SPAN is executed: {TRACE_ID}")
    # When the 'with' block goes out of scope, 'span' is closed for you

meter = metrics.get_meter(__name__)

work_counter = meter.create_counter(
    "work.counter", unit="1", description="Counts the amount of work done"
)

work_counter.add(1, {"work.type": "example"})



# Shut down the OTEL SDK
oti.shutdown()
```

Execute the `oti.shutdown()` during the shutdown process.
It makes sure that the traces and metrics will surely be exported before termination.

It is also possible to use environment variables to configure the `OTI()` class within the following variables:

- `OTEL_SERVICE_NAME`: The name of the service. default: `"UNDEFINED_SERVICE"`.
- `OTEL_SERVICE_VERSION`: The version of the service. Default: `"UNDEFINED_SERVICE_VERSION"`.
- `OTEL_SERVICE_NAMESPACE`: The service namespace. Default: `"UNDEFINED_SERVICE_NS"`.
- `OTEL_EXPORTER_TYPE`:  The type of the exporter. One of: `"STDOUT" | "OTLPGRPC | OTLPHTTP"`. Default: `"STDOUT"`.
- `OTEL_EXPORTER_URL`: The URL of the collector agent or service. Default: `"http://localhost:4317"`.
- `OTEL_SPAN_PROCESSOR_TYPE`: The type of the span processor. One of: `"SIMPLE" | "BATCH"`. Default `"SIMPLE"`.
- `OTEL_TRACES_SAMPLER`: The sampling type of tracing. One of: `"ALWAYS_OFF" | "ALWAYS_ON" | "TRACEIDRATIO" | "PARENTBASED" | "PARENTBASED_ALWAYS_OFF" | "PARENTBASED_ALWAYS_ON" | "PARENTBASED_TRACEIDRATIO"`. Default: `"PARENTBASED_ALWAYS_ON"`.
- `OTEL_TRACES_SAMPLER_ARG`: It is used, of the `OTEL_TRACES_SAMPLER` config parameter has one of the `"...RATIO"` values. Default: `"1.0"`.
- `OTEL_METRIC_EXPORTER_MODE`:  The operating mechanism of the metric exporter. One of: `"ENDPOINT" | "PERIODIC" | "BOTH"`. Default: `"ENDPOINT"`.
- `OTEL_METRIC_EXPORTER_ENDPOINT_ADDR`: The host part of the metric exporter endpoint. Default: `"localhost"`.
- `OTEL_METRIC_EXPORTER_ENDPOINT_PORT`: The port part of the metric exporter endpoint. Default: `"9464"`.
- `OTEL_METRIC_EXPORT_INTERVAL_MILLIS`: It is used, to set the PeriodicExportingMetricReader config
- `OTEL_METRIC_EXPORT_TIMEOUT_MILLIS`: It is used, to set the PeriodicExportingMetricReader config

The operating mechanism of the metric exporter can be set by the `OTEL_METRIC_EXPORTER_MODE` environment variable. 
In case of `"PERIODIC"` the metrics are exported periodically, and the interval can be set by the `OTEL_METRIC_EXPORT_INTERVAL_MILLIS` variable.
In case of `"ENDPOINT"` the metrics are exported to the endpoint defined by the `OTEL_METRIC_EXPORTER_ENDPOINT_ADDR` and `OTEL_METRIC_EXPORTER_ENDPOINT_PORT` variables.
These two mechanisms can be combined by setting the `OTEL_METRIC_EXPORTER_MODE` to `"BOTH"`.

Read the [API docs](https://tombenke.github.io/otel-inst-py/) on the configuration,
and see also the [examples](examples/) on the usage of this package.

## Development

### Prerequisites

You will need the following tools installed on your machine:
- bash
- git
- Python 3.11
- sed
- [Task](https://taskfile.dev/)
- docker, docker-compose

### Installation

Clone the repository:

```bash
    git clone git@github.com:tombenke/otel-inst-py.git
```

Create a Python virtual environment in the local folder:

```bash
    task venv-create
```

Activate the newly created virtual environment:

```bash
    . venv/bin/activate
```

Install the dependencies:

```bash
    task install-dev-editable
```

Run tests and docs generation:

```bash
    task
```

List the tasks are available for further works:

```bash
task list

task: Available tasks for this project:
* build: 		Build
* clean: 		Clean temporary files and folders
* coverage: 		Test coverage
* dc-down: 		Clean up docker containers
* dc-logs: 		Get all docker container logs
* dc-logsf: 		Get all docker container logs and follow
* dc-stop: 		Stop docker containers
* dc-up: 		Start docker containers
* dc-upd: 		Start docker containers in the background
* default: 		Executes all the tests then build the binary.
* docs: 		Generate module documentation into the docs/ folder
* format: 		Autoformat the source files
* install: 		Install the package and its dependencies
* install-dev: 		Install the package and its dependencies for development
* install-dev-editable: Install the package and its dependencies for development with editablility
* install-git-hooks: 	Install git hooks
* lint: 		Run python linter
* pre-commit: 		Runs the QA tasks from a git pre-commit hook
* publish-package: 	Publish the package to PyPI
* test: 		Run all the tests.
* test-verbose: 	Run all the go tests.
* venv-create: 		Create a new Python Virtual Environment under the local folder
```

## License
The scripts and documentation in this project are released under the [MIT License](LICENSE)

## References:
- [Open Telemetry website](https://opentelemetry.io/)
- [OpenTelemetry-Python - The Python implementation of OpenTelemetry.](https://opentelemetry-python.readthedocs.io/en/stable/index.html)
- [OpenTelemetry Python API](https://opentelemetry-python.readthedocs.io/en/latest/api/index.html)
- [Manual OTEL Instrumentation with Python](https://opentelemetry.io/docs/instrumentation/python/manual/)
- [Cookbook for common OTEL scenarios with Python](https://opentelemetry.io/docs/instrumentation/python/cookbook/)
- [Jaeger](https://www.jaegertracing.io/)
