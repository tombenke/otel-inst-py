"""
This example uses the tracing API and instruments the OTI with the default config values.
"""

from opentelemetry import metrics

from oti import OTI

# Configure the OTEL SDK
oti = OTI()

# Use the OTEL via API only without the OTI (SDK instrumentation)
meter = metrics.get_meter(__name__)

work_counter = meter.create_counter(
    "work.counter", unit="1", description="Counts the amount of work done"
)


def do_work(work_item):
    """Do some example work"""
    work_counter.add(1, {"work.type": work_item})
    print("doing some work...")


i = 0
while i < 10:
    do_work("test_work")
    i = i + 1

# Shut down the OTEL SDK
oti.shutdown()
