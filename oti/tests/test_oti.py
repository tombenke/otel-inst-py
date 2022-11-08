"""Test the oti module"""
import logging
import unittest
import time
from opentelemetry import trace  # Import the OTEL API
import requests
from oti import OTI, OTIConfig, ExporterConfig, SamplingConfig


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

        service_name = "test_trace_otelgrpc"
        oti = OTI(
            OTIConfig(
                service_name=service_name,
                service_namespace="examples",
                service_instance_id="stot_42",
                service_version="v1.0.0",
                # exporter_config=ExporterConfig(exporter_type="OTLPGRPC"),
                exporter_config=ExporterConfig(
                    exporter_type="OTLPHTTP",
                    exporter_url="http://localhost:4318/v1/traces",
                ),
                sampling_config=SamplingConfig(
                    trace_sampling_type="PARENTBASED_ALWAYS_ON"
                ),
            )
        )
        tracer = trace.get_tracer(__name__)
        trace_id = None
        with tracer.start_as_current_span("span-name") as span:
            # do some work that 'span' will track
            trace_id = str(hex(span.get_span_context().trace_id)[2:])
            log.debug("TRACER / SPAN is executed: %s", trace_id)
            # When the 'with' block goes out of scope, 'span' is closed for you

        oti.shutdown()
        traces = fetch_traces_by_service(service_name)
        log.debug(traces)
        trace_0 = traces["data"][0]
        self.assertEqual("span-name", trace_0["spans"][0]["operationName"])
