from oti import OTI, OTIConfig, ExporterConfig, SamplingConfig

oti = OTI(
    OTIConfig(
        service_name="simple_trace_otelgrpc",
        exporter_config=ExporterConfig(exporter_type="OTELGRPC"),
        sampling_config=SamplingConfig(trace_sampling_type="ALWAYS"),
    )
)

with oti.tracer.start_as_current_span("simple-trace-example") as span:
    # do some work that 'span' will track
    trace_id = str(hex(span.get_span_context().trace_id)[2:])
    print(f"TRACER / SPAN is executed: {trace_id}")
    # When the 'with' block goes out of scope, 'span' is closed for you

oti.shutdown()
