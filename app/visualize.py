import json
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

def load_results(file_path):
    """Load benchmark results from a JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def create_bar_chart(results, operation_prefix, title, output_file):
    """Create a bar chart comparing Redis and Valkey for a specific operation type"""
    operations = [op for op in results["redis"].keys() if op.startswith(operation_prefix)]
    
    operations.sort(key=lambda x: int(x.split('_')[1]) if '_' in x else 0)
    
    x_labels = [f"{op.split('_')[1]}B" if '_' in op else op for op in operations]
    
    redis_times = [results["redis"][op]["mean"] for op in operations]
    valkey_times = [results["valkey"][op]["mean"] for op in operations]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bar_width = 0.35
    
    r1 = np.arange(len(operations))
    r2 = [x + bar_width for x in r1]
    
    ax.bar(r1, redis_times, width=bar_width, label='Redis', color='red', alpha=0.7)
    ax.bar(r2, valkey_times, width=bar_width, label='Valkey', color='blue', alpha=0.7)
    
    ax.set_xlabel('Data Size')
    ax.set_ylabel('Time (seconds)')
    ax.set_title(title)
    ax.set_xticks([r + bar_width/2 for r in range(len(operations))])
    ax.set_xticklabels(x_labels)
    
    ax.legend()
    
    ax.grid(True, linestyle='--', alpha=0.7)
    
    for i, v in enumerate(redis_times):
        ax.text(i - 0.1, v + 0.01, f"{v:.3f}s", color='black', fontweight='bold', fontsize=8)
    
    for i, v in enumerate(valkey_times):
        ax.text(i + bar_width - 0.1, v + 0.01, f"{v:.3f}s", color='black', fontweight='bold', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def create_comparison_chart(results, output_file):
    """Create a chart comparing Redis and Valkey across all operations"""
    operations = list(results["redis"].keys())
    
    differences = []
    labels = []
    
    for op in operations:
        redis_time = results["redis"][op]["mean"]
        valkey_time = results["valkey"][op]["mean"]
        
        if redis_time > 0:
            diff_percent = ((valkey_time - redis_time) / redis_time) * 100
            differences.append(diff_percent)
            
            if '_' in op:
                op_type, size = op.split('_')
                labels.append(f"{op_type.upper()} {size}B")
            else:
                labels.append(op.upper())
    
    sorted_indices = np.argsort(differences)
    sorted_diffs = [differences[i] for i in sorted_indices]
    sorted_labels = [labels[i] for i in sorted_indices]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bars = ax.barh(sorted_labels, sorted_diffs)
    
    for i, bar in enumerate(bars):
        if sorted_diffs[i] < 0:
            bar.set_color('green')  # Valkey is faster
        else:
            bar.set_color('red')    # Redis is faster
    
    ax.set_xlabel('Performance Difference (%)')
    ax.set_title('Valkey vs Redis Performance Comparison')
    
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.7)
    
    for i, v in enumerate(sorted_diffs):
        if v < 0:
            ax.text(v - 5, i, f"{abs(v):.1f}% faster", ha='right', va='center', color='black', fontweight='bold')
        else:
            ax.text(v + 1, i, f"{v:.1f}% slower", ha='left', va='center', color='black', fontweight='bold')
    
    ax.text(max(sorted_diffs) * 0.8, len(sorted_labels) * 0.9, "Valkey faster ←", ha='center', fontsize=12, color='green')
    ax.text(min(sorted_diffs) * 0.8, len(sorted_labels) * 0.9, "→ Redis faster", ha='center', fontsize=12, color='red')
    
    ax.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def visualize_results(results_file):
    """Create visualizations from benchmark results"""
    output_dir = os.path.join(os.path.dirname(results_file), 'charts')
    os.makedirs(output_dir, exist_ok=True)
    
    results = load_results(results_file)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    create_bar_chart(results, "set_", "SET Operation Performance", 
                    os.path.join(output_dir, f"set_performance_{timestamp}.png"))
    
    create_bar_chart(results, "get_", "GET Operation Performance", 
                    os.path.join(output_dir, f"get_performance_{timestamp}.png"))
    
    create_bar_chart(results, "lpush_", "LPUSH Operation Performance", 
                    os.path.join(output_dir, f"lpush_performance_{timestamp}.png"))
    
    create_comparison_chart(results, os.path.join(output_dir, f"overall_comparison_{timestamp}.png"))
    
    print(f"Visualizations created in {output_dir}")

if __name__ == "__main__":
    results_file = '/app/results/benchmark_results.json'
    if os.path.exists(results_file):
        visualize_results(results_file)
    else:
        print(f"Results file not found: {results_file}")
        print("Run the benchmark first to generate results.")
