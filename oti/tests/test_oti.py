"""Test the oti module"""
import logging
import unittest
from unittest.mock import patch
from io import StringIO
from oti import OTI, OTIConfig, ExporterConfig, SamplingConfig

import requests
import sys
import time


def fetch_traces_by_service(service):
    """Retrieve the trace from the Jaeger server selected by its trace_id"""

    trace_url = f"http://localhost:16686/api/traces?service={service}&lookback=20m&prettyPrint=true&limit=1"
    num_of_retries = 4
    time_interval = 0.5
    for _ in range(num_of_retries):
        with requests.get(trace_url) as response:
            content = response.json()
            if content["errors"] == None and len(content["data"]) > 0:
                return content
            time.sleep(time_interval)


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

        oti = OTI(
            OTIConfig(
                service_name="simple_trace_otelgrpc",
                exporter_config=ExporterConfig(exporter_type="OTELGRPC"),
                sampling_config=SamplingConfig(trace_sampling_type="ALWAYS"),
            )
        )
        trace_id = None
        with oti.tracer.start_as_current_span("span-name") as span:
            # do some work that 'span' will track
            trace_id = str(hex(span.get_span_context().trace_id)[2:])
            log.debug(f"TRACER / SPAN is executed: {trace_id}")
            # When the 'with' block goes out of scope, 'span' is closed for you

        oti.shutdown()
        traces = fetch_traces_by_service("unknown_service")
        log.debug(traces)
        trace = traces["data"][0]
        # self.assertEqual(trace_id, trace["traceID"])
        self.assertEqual("span-name", trace["spans"][0]["operationName"])
