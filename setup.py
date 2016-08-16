import os
from distutils.core import setup

setup(
        name="es_search_exporter",
        version="0.1.0",
        author="Jarod Watkins",
        author_email="jarod@42lines.net",
        description = ("Elasticsearch search exporter for the Prometheus monitoring system."),
        long_description = ("See https://github.com/ipstatic/es_search_exporter/blob/master/README.md for documentation."),
        license = "MIT",
        keywords = "prometheus exporter network monitoring elastic search",
        url = "https://github.com/ipstatic/es_search_exporter",
        scripts = ["scripts/es_search_exporter"],
        packages=["es_search_exporter"],
        test_suite="tests",
        install_requires=["prometheus_client>=0.0.14", "pyyaml>=3.11", "requests>=2.10.0", "requests-kerberos>=0.10.0"],
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Information Technology",
            "Intended Audience :: System Administrators",
            "Topic :: System :: Monitoring",
            "License :: OSI Approved :: MIT License",
        ],
)
