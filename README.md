# Elasticsearch Search Exporter

This is an exporter that allows you to execute queries against an Elasticsearch
cluster and return the number of documents found for use by the
[Prometheus](https://prometheus.io) monitoring system.

## Installation 

```
pip install es_search_exporter
```

### ES Search Exporter Configuration

You will need to add your Elasticsearch query to the searches hash in es_search.yml.
This could also be a JSON file as well if that would make it easier (JSON is valid
YAML, and most tools like Kibana can produce a JSON version of your query).

### Prometheus Job Configuration

```
scrape_configs:
  - job_name: 'es_search_exporter'
    static_configs:
      - targets:
        - elastichost.example.com
    params:
      search: ['example']
    relabel_configs:
      - source_labels: [__address__]
        regex: (.*?)(:80)?
        target_label: __param_address
        replacement: ${1}
      - source_labels: [__param_address]
        regex: (.*)
        target_label: instance
        replacement: ${1}
      - source_labels: []
        regex: .*
        target_label: __address__
        replacement: 127.0.0.1:9920 # ES Search Exporter
```

## Developing Locally

To work on this locally without installing the package, execute:

```
./scripts/run_locally --kerberos --tls
```

This script will setup your path correctly and run the exporter.
