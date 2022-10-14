"""Test the oti module"""
import unittest
from oti import OTIConfig, ExporterConfig, SamplingConfig


class OTIConfigTestCase(unittest.TestCase):
    """The OTIConfig test cases"""

    def test_OTIConfig_defaults(self) -> None:
        """Test the OTIConfig class"""

        config = OTIConfig()
        self.assertEqual(config.service_name, "UNDEFINED_SERVICE")
        self.assertEqual(config.span_processor_type, "SIMPLE")
        self.assertEqual(config.exporter_config.exporter_type, "STDOUT")
        self.assertEqual(config.exporter_config.collector_url, "localhost:4317")
        self.assertEqual(config.sampling_config.trace_sampling_type, "NEVER")
        self.assertEqual(config.sampling_config.trace_sampling_ratio, 1.0)

    def test_OTIConfig_defaults(self) -> None:
        """Test the OTIConfig class"""

        config = OTIConfig(
            service_name="test_service",
            exporter_config=ExporterConfig(exporter_type="OTELGRPC"),
            sampling_config=SamplingConfig(trace_sampling_type="ALWAYS"),
        )
        self.assertEqual(config.service_name, "test_service")
        self.assertEqual(config.span_processor_type, "SIMPLE")
        self.assertEqual(config.exporter_config.exporter_type, "OTELGRPC")
        self.assertEqual(config.exporter_config.collector_url, "localhost:4317")
        self.assertEqual(config.sampling_config.trace_sampling_type, "ALWAYS")
        self.assertEqual(config.sampling_config.trace_sampling_ratio, 1.0)
