"""Test the oti module"""

import unittest
import os
from oti import OTIConfig, ExporterConfig, SamplingConfig
from oti.config import (
    DEFAULT_SERVICE_NAME,
    DEFAULT_SERVICE_NAMESPACE,
    DEFAULT_SERVICE_VERSION,
    DEFAULT_OTEL_EXPORTER_TYPE,
    DEFAULT_OTEL_EXPORTER_URL,
    DEFAULT_SPAN_PROCESSOR_TYPE,
    DEFAULT_OTEL_SAMPLING_TYPE,
    DEFAULT_OTEL_SAMPLING_RATIO,
)


class OTIConfigTestCase(unittest.TestCase):
    """The OTIConfig test cases"""

    def test_config_defaults(self) -> None:
        """Test the OTIConfig class using default values"""

        config = OTIConfig()
        self.assertEqual(config.service_name, DEFAULT_SERVICE_NAME)
        self.assertEqual(config.service_namespace, DEFAULT_SERVICE_NAMESPACE)
        self.assertEqual(config.service_version, DEFAULT_SERVICE_VERSION)
        self.assertEqual(config.span_processor_type, DEFAULT_SPAN_PROCESSOR_TYPE)
        self.assertEqual(
            config.exporter_config.exporter_type, DEFAULT_OTEL_EXPORTER_TYPE
        )
        self.assertEqual(config.exporter_config.exporter_url, DEFAULT_OTEL_EXPORTER_URL)
        self.assertEqual(
            config.sampling_config.trace_sampling_type, DEFAULT_OTEL_SAMPLING_TYPE
        )
        self.assertEqual(config.sampling_config.trace_sampling_ratio, 1.0)

    def test_config_with_config_object(self) -> None:
        """Test the OTIConfig class using initial config parameters"""

        expected_service_name = "test_service"
        expected_exporter_type = "OTELGRPC"
        expected_trace_sampling_type = "ALWAYS"
        config = OTIConfig(
            service_name=expected_service_name,
            exporter_config=ExporterConfig(exporter_type=expected_exporter_type),
            sampling_config=SamplingConfig(
                trace_sampling_type=expected_trace_sampling_type
            ),
        )
        self.assertEqual(config.service_name, expected_service_name)
        self.assertEqual(config.span_processor_type, DEFAULT_SPAN_PROCESSOR_TYPE)
        self.assertEqual(config.exporter_config.exporter_type, expected_exporter_type)
        self.assertEqual(config.exporter_config.exporter_url, DEFAULT_OTEL_EXPORTER_URL)
        self.assertEqual(
            config.sampling_config.trace_sampling_type, expected_trace_sampling_type
        )
        self.assertEqual(
            config.sampling_config.trace_sampling_ratio,
            float(DEFAULT_OTEL_SAMPLING_RATIO),
        )

    def test_config_with_env(self) -> None:
        """Test the OTIConfig class using environment variables"""

        # The expected values for parameters used via environment parameters
        expected_service_name = "test-service"
        expected_traces_sampler = "always_off"
        expected_traces_sampler_arg = "0.01"
        test_set_input = {
            "OTEL_SERVICE_NAME": expected_service_name,
            "OTEL_TRACES_SAMPLER": expected_traces_sampler,
            "OTEL_TRACES_SAMPLER_ARG": expected_traces_sampler_arg,
        }
        # Set the environment using the expected values
        os.environ.update(test_set_input)

        config = OTIConfig()
        self.assertEqual(expected_service_name, config.service_name)
        self.assertEqual(config.span_processor_type, DEFAULT_SPAN_PROCESSOR_TYPE)
        self.assertEqual(
            config.exporter_config.exporter_type, DEFAULT_OTEL_EXPORTER_TYPE
        )
        self.assertEqual(config.exporter_config.exporter_url, DEFAULT_OTEL_EXPORTER_URL)
        self.assertEqual(
            expected_traces_sampler, config.sampling_config.trace_sampling_type
        )
        self.assertEqual(
            config.sampling_config.trace_sampling_ratio,
            float(expected_traces_sampler_arg),
        )
