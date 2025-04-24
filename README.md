# Redis vs Valkey Benchmark

This project provides a containerized application to benchmark and compare the performance of Redis OSS and Valkey.

## Overview

The benchmark application tests various Redis/Valkey operations:
- SET operations with different data sizes (10B, 100B, 1KB, 10KB)
- GET operations with different data sizes
- INCR operations
- LPUSH operations with different data sizes
- LPOP operations

Each test is repeated multiple times to ensure statistical significance.

## Requirements

- Docker
- Docker Compose

## Usage

### Quick Start

Use the provided shell script to run the benchmark:

```bash
git clone https://github.com/rohitg00/redis-valkey-oss.git
cd redis-valkey-oss
./run.sh
```

This will build and run the containers, execute the benchmark, and generate visualizations.

### Manual Execution

Alternatively, you can run the benchmark manually:

```bash
docker-compose up --build
```

### View Results

After the benchmark completes:
1. View the JSON results in `results/benchmark_results.json`
2. View the generated charts in `results/charts/`

## Configuration

You can modify the benchmark parameters in the `app/app.py` file:

- `NUM_OPERATIONS`: Number of operations for each test
- `DATA_SIZES`: Data sizes to test (in bytes)
- `REPEAT_COUNT`: Number of times to repeat each test

## Architecture

The application consists of three containers:
1. Redis OSS container
2. Valkey container
3. Python benchmark application container

The benchmark application connects to both Redis and Valkey instances, runs the tests, and saves the results.

## Results

### JSON Results

Results are saved in JSON format in the `results` directory. The file includes:
- Raw timing data for each test
- Statistical metrics (mean, median, min, max)
- Metadata about the benchmark run

A summary is also printed to the console after the benchmark completes.

### Visualizations

The benchmark automatically generates the following charts:
- SET operation performance across different data sizes
- GET operation performance across different data sizes
- LPUSH operation performance across different data sizes
- Overall performance comparison between Redis and Valkey

These visualizations make it easy to identify performance differences between Redis and Valkey for different operations and data sizes.
