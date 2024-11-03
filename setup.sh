#!/bin/bash

# Create the main project directory
mkdir -p stock_pipeline/{docker,src/extractors,src/transformers,src/loaders,src/quality,dags,dashboard,config}

# Create the Docker files
touch stock_pipeline/docker/Dockerfile
touch stock_pipeline/docker/docker-compose.yml

# Create the extractors files
touch stock_pipeline/src/extractors/yahoo_finance.py
touch stock_pipeline/src/extractors/alpha_vantage.py

# Create the transformers file
touch stock_pipeline/src/transformers/price_transformer.py

# Create the loaders file
touch stock_pipeline/src/loaders/postgres_loader.py

# Create the quality file
touch stock_pipeline/src/quality/data_quality.py

# Create the DAGs file
touch stock_pipeline/dags/stock_pipeline_dag.py

# Create the dashboard file
touch stock_pipeline/dashboard/app.py

# Create the config file
touch stock_pipeline/config/config.yaml

echo "Project structure created successfully!"
