"""Test the oti module"""

import asyncio
import logging
import re
import unittest
import time
import httpx
from opentelemetry import trace, metrics  # Import the OTEL API
import requests
from oti import OTI, OTIConfig, ExporterConfig, SamplingConfig
from oti.config import PeriodicMetricReaderConfig, MetricReaderEndpointConfig


def fetch_traces_by_service(service):
    """Retrieve the traces from Tempo Traces Database through Grafana selected by its rootServiceName"""
    trace_url = f"http://localhost:3000/api/datasources/proxy/uid/tempo/api/search?q=%7BrootServiceName%3D%22{service}%22%7D"
    num_of_retries = 4
    time_interval = 0.5
    for _ in range(num_of_retries):
        with requests.get(trace_url, timeout=1) as response:
            if response.status_code == 200:
                content = response.json()
                if len(content["traces"]) > 0:
                    return content
                print("Trace not found, waiting 0.5 sec...")
                time.sleep(time_interval)
    return None


async def fetch_metric_by_service():
    """Retrieve the metric from Prometheus Metric Database"""
    prometheus_url = "http://localhost:3000/api/datasources/proxy/uid/prometheus/api/v1/query?query=work_counter_total"
    num_of_retries = 10
    time_interval = 1
    for _ in range(num_of_retries):
        async with httpx.AsyncClient() as client:
            response = await client.get(prometheus_url)
            content = response.json()
            if content["status"] == "success" and len(content["data"]["result"]) > 0:
                return content["data"]["result"][0]
            print("Metric not found, waiting 1 sec...")
            time.sleep(time_interval)
    return None


async def fetch_metric_from_server():
    """Retrieve the metric from the local server"""
    server_url = "http://localhost:9464/metrics"
    num_of_retries = 10
    time_interval = 1
    for _ in range(num_of_retries):
        async with httpx.AsyncClient() as client:
            response = await client.get(server_url)
        content = response.text
        if response.status_code == 200 and "TYPE work_counter_total counter" in content:
            # Use regex to find the line containing the work_counter_total value
            match = re.search(
                r"^work_counter_total\{.*\} \d+\.\d+$", content, re.MULTILINE
            )
            return match.group()
        print("Metric not found, waiting 1 sec...")
        time.sleep(time_interval)
    return None


class OtiTestCase(unittest.IsolatedAsyncioTestCase):
    """The OTI test cases"""

    async def test_oti(self) -> None:
        """Test the OTI class with BOTH operating mode (PERIODIC and ENDPOINT at the same time)"""
        # The different operating modes must be tested at the same time because the opentelemetry's set_meter_provider
        # method (which is responsible for setting the global default meter provider) can be called only once.

        logging.basicConfig(
            filename="LOG",
            filemode="w",
            format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
            datefmt="%H:%M:%S",
            level=logging.DEBUG,
        )
        log = logging.getLogger("LOG")

        service_name = "test_otelgrpc"
        oti_config = OTIConfig(
            service_name=service_name,
            service_namespace="examples",
            service_instance_id="stot_42",
            service_version="v1.0.0",
            exporter_config=ExporterConfig(exporter_type="OTLPGRPC"),
            sampling_config=SamplingConfig(trace_sampling_type="PARENTBASED_ALWAYS_ON"),
            metric_exporter_mode_config="BOTH",
            periodic_metric_reader_config=PeriodicMetricReaderConfig(1000, 500),
            metric_exporter_endpoint_config=MetricReaderEndpointConfig(
                "localhost", "9464"
            ),
        )

        oti = OTI(oti_config)

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
        time.sleep(5)

        # periodic test
        metric = await fetch_metric_by_service()
        self.assertIsNotNone(metric)
        self.assertEqual("1", metric["value"][1])

        traces = fetch_traces_by_service(service_name)
        log.debug(traces)
        self.assertEqual("span-name", traces["traces"][0]["rootTraceName"])

        # endpoint test
        metric2 = await fetch_metric_from_server()
        match = re.search(r'work_counter_total\{work_type="test"\} (\d+\.\d+)', metric2)
        self.assertIsNotNone(match)
        self.assertEqual("1.0", match.group(1))

        await asyncio.sleep(5)
        oti.shutdown()
