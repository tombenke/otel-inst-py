from oti import OTI, OTIConfig, ExporterConfig, SamplingConfig

oti = OTI(
    OTIConfig(
        service_name="simple_trace_stdout",
        exporter_config=ExporterConfig(exporter_type="STDOUT"),
        sampling_config=SamplingConfig(trace_sampling_type="ALWAYS"),
    )
)

with oti.tracer.start_as_current_span("span-name") as span:
    # do some work that 'span' will track
    print(f"TRACER / SPAN is executed: {span.get_span_context().trace_id}")
    # When the 'with' block goes out of scope, 'span' is closed for you

oti.shutdown()
