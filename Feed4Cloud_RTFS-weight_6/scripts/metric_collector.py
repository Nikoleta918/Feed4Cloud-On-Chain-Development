from prometheus_client import start_http_server
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from threading import Lock

class MetricCollector():


    def __init__(self, port, metric_prefix):
        self.port = port
        self.metric_prefix = metric_prefix
        self.metric_map = dict()
        self.metric_value = dict()
        self.meter = get_meter_provider().get_meter("getting-started")
        # Start Prometheus client
        start_http_server(port=port, addr="0.0.0.0")
        # Initialize PrometheusMetricReader which pulls metrics from the SDK
        # on-demand to respond to scrape requests
        reader = PrometheusMetricReader(prefix=metric_prefix)
        provider = MeterProvider(metric_readers=[reader])
        set_meter_provider(provider)
        self.lock = Lock()


    def collect_metric(self, name, value):
        with self.lock:
            metric = self.metric_map.get(name)
            last_value = self.metric_value.get(name)
            if (metric == None):
                self.metric_map[name] = self.meter.create_up_down_counter(name)
                self.metric_value[name] = value
                metric = self.metric_map.get(name)
                metric.add(float(value))
            else:
                metric.add(float(value-last_value))
                self.metric_value[name] = value
