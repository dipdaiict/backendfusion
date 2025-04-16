from opentelemetry import trace
from app.config import otel_settings
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

def setup_tracer(service_name: str = None):
    """Initialize OpenTelemetry tracing."""
    resource = Resource.create({"service.name": otel_settings.service_name})
    tracer_provider = TracerProvider(resource=resource)

    # Configure OTLP HTTP exporter (Jaeger)
    otlp_exporter = OTLPSpanExporter(endpoint=otel_settings.otlp_endpoint)
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)

    trace.set_tracer_provider(tracer_provider)
    return tracer_provider