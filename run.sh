

echo "Starting Redis vs Valkey benchmark..."
echo "This will build and run the containers, execute the benchmark, and generate visualizations."

docker compose up --build

echo "Benchmark complete. Results are available in the 'results' directory."
echo "- JSON results: results/benchmark_results.json"
echo "- Charts: results/charts/"

if [ -d "results/charts" ] && [ "$(ls -A results/charts)" ]; then
    echo "Charts generated:"
    ls -la results/charts
else
    echo "No charts were generated. Check for errors in the benchmark output."
fi
