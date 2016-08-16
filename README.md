# Elasticsearch Search Exporter

This is an exporter that allows you to execute queries against an Elasticsearch
cluster and return the number of documents found for use by the
[Prometheus](https://prometheus.io) monitoring system.

## Installation 

```
pip install es_search_exporter
```

## Developing Locally

To work on this locally without installing the package, execute:

```
./scripts/run_locally --kerberos --tls
```

This script will setup your path correctly and run the exporter.
