otel-inst-py
============

[![Quality Check Status](https://github.com/tombenke/otel-inst-py/workflows/Quality%20Check/badge.svg)](https://github.com/tombenke/otel-inst-py)
[![Release Status](https://github.com/tombenke/otel-inst-py/workflows/Release/badge.svg)](https://github.com/tombenke/otel-inst-py)
![Coverage](./coverage.svg)

## About

Python package that provides the basic features required for Open-Telemetry instrumentation.
It makes easier the manual instrumentation of a python application.

See also the [API docs](https://tombenke.github.io/otel-inst-py/) of the package.

### Prerequisites

You will need the following tools installed on your machine:
- bash
- git
- Python 3.10
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

## Examples

See the [examples](examples/) on the usage of this package.

## License
The scripts and documentation in this project are released under the [MIT License](LICENSE)

## References:
- [Open Telemetry website](https://opentelemetry.io/)
- [OpenTelemetry-Python - The Python implementation of OpenTelemetry.](https://opentelemetry-python.readthedocs.io/en/stable/index.html)
- [OpenTelemetry Python API](https://opentelemetry-python.readthedocs.io/en/latest/api/index.html)
- [Manual OTEL Instrumentation with Python](https://opentelemetry.io/docs/instrumentation/python/manual/)
- [Cookbook for common OTEL scenarios with Python](https://opentelemetry.io/docs/instrumentation/python/cookbook/)
- [Jaeger](https://www.jaegertracing.io/)
