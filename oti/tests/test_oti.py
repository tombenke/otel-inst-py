"""Test the oti module"""
import logging
import unittest
import time
from opentelemetry import trace, metrics  # Import the OTEL API
import requests
from oti import OTI, OTIConfig, ExporterConfig, SamplingConfig
from oti.config import PeriodicMetricReaderConfig


def fetch_traces_by_service(service):
    """Retrieve the trace from the Jaeger server selected by its trace_id"""

    trace_url = f"http://localhost:16686/api/traces?service={service}&lookback=20m&prettyPrint=true&limit=1"
    num_of_retries = 4
    time_interval = 0.5
    for _ in range(num_of_retries):
        with requests.get(trace_url, timeout=1) as response:
            content = response.json()
            if content["errors"] is None and len(content["data"]) > 0:
                return content
            time.sleep(time_interval)
    return None


def fetch_metric_by_service():
    """Retrieve the trace from the Jaeger server selected by its trace_id"""

    prometheus_url = "http://localhost:9090/api/v1/query?query=promexample_work_counter"
    num_of_retries = 20
    time_interval = 1
    for _ in range(num_of_retries):
        with requests.get(prometheus_url, timeout=1) as response:
            content = response.json()
            if content["status"] == "success" and len(content["data"]["result"]) > 0:
                return content["data"]["result"][0]
            print("Metric not found, waiting 1 sec...")
            time.sleep(time_interval)
    return None


class OtiTestCase(unittest.TestCase):
    """The OTI test cases"""

    def test_oti(self) -> None:
        """Test the OTI class"""

        logging.basicConfig(
            filename="LOG",
            filemode="w",
            format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
            datefmt="%H:%M:%S",
            level=logging.DEBUG,
        )
        log = logging.getLogger("LOG")

        service_name = "test_otelgrpc"
        oti = OTI(
            OTIConfig(
                service_name=service_name,
                service_namespace="examples",
                service_instance_id="stot_42",
                service_version="v1.0.0",
                exporter_config=ExporterConfig(exporter_type="OTLPGRPC"),
                sampling_config=SamplingConfig(
                    trace_sampling_type="PARENTBASED_ALWAYS_ON"
                ),
                periodic_metric_reader_config=PeriodicMetricReaderConfig(1000),
            )
        )
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("span-name") as span:
            # do some work that 'span' will track
            trace_id = str(hex(span.get_span_context().trace_id)[2:])
            log.debug("TRACER / SPAN is executed: %s", trace_id)
            # When the 'with' block goes out of scope, 'span' is closed for you

        meter = metrics.get_meter(__name__)

        work_counter = meter.create_counter(
            "work.counter", unit="1", description="Counts the amount of work done"
        )

        work_counter.add(1, {"work.type": "test"})

        oti.shutdown()

        metric = fetch_metric_by_service()
        self.assertIsNotNone(metric)
        self.assertEqual("1", metric["value"][1])

        traces = fetch_traces_by_service(service_name)
        log.debug(traces)
        trace_0 = traces["data"][0]
        self.assertEqual("span-name", trace_0["spans"][0]["operationName"])
