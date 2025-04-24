import redis
import time
import statistics
import os
import json
from datetime import datetime

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
VALKEY_HOST = os.environ.get('VALKEY_HOST', 'valkey')
VALKEY_PORT = int(os.environ.get('VALKEY_PORT', 6379))

NUM_OPERATIONS = 1000
DATA_SIZES = [10, 1000]
REPEAT_COUNT = 3

def connect_to_redis():
    """Connect to Redis OSS instance"""
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def connect_to_valkey():
    """Connect to Valkey instance"""
    return redis.Redis(host=VALKEY_HOST, port=VALKEY_PORT, decode_responses=True)

def generate_data(size):
    """Generate string data of approximately the specified size in bytes"""
    return "x" * size

def benchmark_set(client, prefix, data_size):
    """Benchmark SET operations"""
    data = generate_data(data_size)
    start_time = time.time()
    
    for i in range(NUM_OPERATIONS):
        key = f"{prefix}:set:{i}"
        client.set(key, data)
    
    end_time = time.time()
    return end_time - start_time

def benchmark_get(client, prefix, data_size):
    """Benchmark GET operations"""
    data = generate_data(data_size)
    for i in range(NUM_OPERATIONS):
        key = f"{prefix}:get:{i}"
        client.set(key, data)
    
    start_time = time.time()
    
    for i in range(NUM_OPERATIONS):
        key = f"{prefix}:get:{i}"
        client.get(key)
    
    end_time = time.time()
    return end_time - start_time

def benchmark_incr(client, prefix):
    """Benchmark INCR operations"""
    for i in range(NUM_OPERATIONS):
        key = f"{prefix}:incr:{i}"
        client.set(key, "0")
    
    start_time = time.time()
    
    for i in range(NUM_OPERATIONS):
        key = f"{prefix}:incr:{i}"
        client.incr(key)
    
    end_time = time.time()
    return end_time - start_time

def benchmark_lpush(client, prefix, data_size):
    """Benchmark LPUSH operations"""
    data = generate_data(data_size)
    start_time = time.time()
    
    for i in range(NUM_OPERATIONS):
        key = f"{prefix}:list"
        client.lpush(key, data)
    
    end_time = time.time()
    return end_time - start_time

def benchmark_lpop(client, prefix):
    """Benchmark LPOP operations"""
    data = "x" * 100  # Medium-sized data
    key = f"{prefix}:list:pop"
    
    for i in range(NUM_OPERATIONS):
        client.lpush(key, data)
    
    start_time = time.time()
    
    for i in range(NUM_OPERATIONS):
        client.lpop(key)
    
    end_time = time.time()
    return end_time - start_time

def run_benchmarks():
    """Run all benchmarks and return results"""
    results = {
        "redis": {},
        "valkey": {},
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "num_operations": NUM_OPERATIONS,
            "repeat_count": REPEAT_COUNT
        }
    }
    
    try:
        redis_client = connect_to_redis()
        print("Connected to Redis OSS")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        return None
    
    try:
        valkey_client = connect_to_valkey()
        print("Connected to Valkey")
    except Exception as e:
        print(f"Failed to connect to Valkey: {e}")
        return None
    
    for data_size in DATA_SIZES:
        redis_times = []
        valkey_times = []
        
        for i in range(REPEAT_COUNT):
            redis_time = benchmark_set(redis_client, f"redis:test{i}", data_size)
            redis_times.append(redis_time)
            
            valkey_time = benchmark_set(valkey_client, f"valkey:test{i}", data_size)
            valkey_times.append(valkey_time)
        
        results["redis"][f"set_{data_size}"] = {
            "mean": statistics.mean(redis_times),
            "median": statistics.median(redis_times),
            "min": min(redis_times),
            "max": max(redis_times),
            "raw": redis_times
        }
        
        results["valkey"][f"set_{data_size}"] = {
            "mean": statistics.mean(valkey_times),
            "median": statistics.median(valkey_times),
            "min": min(valkey_times),
            "max": max(valkey_times),
            "raw": valkey_times
        }
    
    for data_size in DATA_SIZES:
        redis_times = []
        valkey_times = []
        
        for i in range(REPEAT_COUNT):
            redis_time = benchmark_get(redis_client, f"redis:get{i}", data_size)
            redis_times.append(redis_time)
            
            valkey_time = benchmark_get(valkey_client, f"valkey:get{i}", data_size)
            valkey_times.append(valkey_time)
        
        results["redis"][f"get_{data_size}"] = {
            "mean": statistics.mean(redis_times),
            "median": statistics.median(redis_times),
            "min": min(redis_times),
            "max": max(redis_times),
            "raw": redis_times
        }
        
        results["valkey"][f"get_{data_size}"] = {
            "mean": statistics.mean(valkey_times),
            "median": statistics.median(valkey_times),
            "min": min(valkey_times),
            "max": max(valkey_times),
            "raw": valkey_times
        }
    
    redis_times = []
    valkey_times = []
    
    for i in range(REPEAT_COUNT):
        redis_time = benchmark_incr(redis_client, f"redis:incr{i}")
        redis_times.append(redis_time)
        
        valkey_time = benchmark_incr(valkey_client, f"valkey:incr{i}")
        valkey_times.append(valkey_time)
    
    results["redis"]["incr"] = {
        "mean": statistics.mean(redis_times),
        "median": statistics.median(redis_times),
        "min": min(redis_times),
        "max": max(redis_times),
        "raw": redis_times
    }
    
    results["valkey"]["incr"] = {
        "mean": statistics.mean(valkey_times),
        "median": statistics.median(valkey_times),
        "min": min(valkey_times),
        "max": max(valkey_times),
        "raw": valkey_times
    }
    
    for data_size in DATA_SIZES:
        redis_times = []
        valkey_times = []
        
        for i in range(REPEAT_COUNT):
            redis_time = benchmark_lpush(redis_client, f"redis:lpush{i}", data_size)
            redis_times.append(redis_time)
            
            valkey_time = benchmark_lpush(valkey_client, f"valkey:lpush{i}", data_size)
            valkey_times.append(valkey_time)
        
        results["redis"][f"lpush_{data_size}"] = {
            "mean": statistics.mean(redis_times),
            "median": statistics.median(redis_times),
            "min": min(redis_times),
            "max": max(redis_times),
            "raw": redis_times
        }
        
        results["valkey"][f"lpush_{data_size}"] = {
            "mean": statistics.mean(valkey_times),
            "median": statistics.median(valkey_times),
            "min": min(valkey_times),
            "max": max(valkey_times),
            "raw": valkey_times
        }
    
    redis_times = []
    valkey_times = []
    
    for i in range(REPEAT_COUNT):
        redis_time = benchmark_lpop(redis_client, f"redis:lpop{i}")
        redis_times.append(redis_time)
        
        valkey_time = benchmark_lpop(valkey_client, f"valkey:lpop{i}")
        valkey_times.append(valkey_time)
    
    results["redis"]["lpop"] = {
        "mean": statistics.mean(redis_times),
        "median": statistics.median(redis_times),
        "min": min(redis_times),
        "max": max(redis_times),
        "raw": redis_times
    }
    
    results["valkey"]["lpop"] = {
        "mean": statistics.mean(valkey_times),
        "median": statistics.median(valkey_times),
        "min": min(valkey_times),
        "max": max(valkey_times),
        "raw": valkey_times
    }
    
    return results

def save_results(results):
    """Save benchmark results to a file"""
    with open('/app/results/benchmark_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("Results saved to /app/results/benchmark_results.json")

def print_summary(results):
    """Print a summary of the benchmark results"""
    print("\n===== BENCHMARK SUMMARY =====")
    print(f"Operations per test: {NUM_OPERATIONS}")
    print(f"Tests repeated: {REPEAT_COUNT} times")
    
    for operation in results["redis"].keys():
        redis_time = results["redis"][operation]["mean"]
        valkey_time = results["valkey"][operation]["mean"]
        
        if redis_time > 0:
            diff_percent = ((valkey_time - redis_time) / redis_time) * 100
            faster = "Redis" if redis_time < valkey_time else "Valkey"
            diff_abs = abs(diff_percent)
            
            print(f"\nOperation: {operation}")
            print(f"Redis: {redis_time:.6f} seconds")
            print(f"Valkey: {valkey_time:.6f} seconds")
            print(f"{faster} is {diff_abs:.2f}% faster")
        else:
            print(f"\nOperation: {operation}")
            print(f"Redis: {redis_time:.6f} seconds")
            print(f"Valkey: {valkey_time:.6f} seconds")
            print("Unable to calculate percentage difference (division by zero)")

if __name__ == "__main__":
    print("Starting Redis vs Valkey benchmark...")
    
    os.makedirs('/app/results', exist_ok=True)
    
    results = run_benchmarks()
    
    if results:
        save_results(results)
        
        print_summary(results)
    else:
        print("Benchmark failed. Check connections to Redis and Valkey.")
