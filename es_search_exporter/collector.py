import json
import requests
from requests_kerberos import HTTPKerberosAuth
import time
from prometheus_client import Metric, CollectorRegistry, generate_latest

def collect_es(name, config, host, kerberos, tls):
    """Execute a search against Elasticsearch and return prometheus text format for it"""
    try:
        a = None
        if kerberos:
            a = HTTPKerberosAuth()
        s = ''
        if tls:
            s = 's'
        r = requests.get("http{}://{}/{}/_search".format(s, host, config['index']),
            data = json.dumps({"query": config['query'], "size": 0}),
            auth = a,
        )
    except:
        raise Exception('Cannot connect to Elasticsearch host: {}'.format(host))
    if r.status_code == 200:
        count = r.json()['hits']['total']
        successful = r.json()['_shards']['successful']
        failed = r.json()['_shards']['failed']
        total = r.json()['_shards']['total']
        duration = float(r.json()['took']) / 1000
        timed_out = r.json()['timed_out']
    else: 
        raise Exception('Query failed: {}'.format(r.json()))

    metrics = {}
    metrics['results'] = Metric('es_search_{}_results_total'.format(name), 'Number of matching results from Elasticsearch', 'gauge')
    metrics['results'].add_sample('es_search_{}_results_total'.format(name), value=count, labels=None)
    metrics['successful'] = Metric('es_search_{}_shards_successful_total'.format(name), 'Number of shards where the query returned successfully', 'gauge')
    metrics['successful'].add_sample('es_search_{}_shards_successful_total'.format(name), value=successful, labels=None)
    metrics['failed'] = Metric('es_search_{}_shards_failed_total'.format(name), 'Number of shards where the query failed', 'gauge')
    metrics['failed'].add_sample('es_search_{}_shards_failed_total'.format(name), value=failed, labels=None)
    metrics['total'] = Metric('es_search_{}_shards_total'.format(name), 'Number of shards queried', 'gauge')
    metrics['total'].add_sample('es_search_{}_shards_total'.format(name), value=total, labels=None)
    metrics['timed_out'] = Metric('es_search_{}_timed_out'.format(name), 'Did the query time out', 'gauge')
    metrics['timed_out'].add_sample('es_search_{}_timed_out'.format(name), value=timed_out, labels=None)
    metrics['duration'] = Metric('es_search_{}_duration_seconds'.format(name), 'Time Elasticsearch search took, in seconds', 'gauge')
    metrics['duration'].add_sample('es_search_{}_duration_seconds'.format(name), value=duration, labels=None)

    class Collector():
        def collect(self):
            return metrics.values()
    registry = CollectorRegistry()
    registry.register(Collector())
    return generate_latest(registry)
