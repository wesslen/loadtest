import json
import itertools
import random
import os
import datetime
import csv
import typer
from loadtest.load_tester import LoadTester

app = typer.Typer()


def construct_test_matrix(config_file):
    with open(config_file, "r") as f:
        config = json.load(f)

    return list(
        itertools.product(
            config["endpoints"],
            config["request_types"],
            config["payload_sizes"],
            config["concurrency_levels"],
        )
    )


def fractional_design(matrix, fraction=0.5):
    sample_size = int(len(matrix) * fraction)
    return random.sample(matrix, sample_size)


def save_results_to_csv(results, filename):
    headers = [
        "Endpoint",
        "Request Type",
        "Payload Size",
        "Concurrency",
        "Duration",
        "Creations",
        "Failures",
    ]
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(results)


@app.command()
def main(
    design_type: str = typer.Option(
        "full", help="The design type of the test matrix: 'full' or 'fractional'."
    ),
    fraction: float = typer.Option(
        None,
        help="The fraction of the test matrix to use, required only if design_type is 'fractional'.",
    ),
):
    """
    Executes a series of load tests based on configurations defined in a JSON file, allowing for either full or
    fractional testing. The script generates a test matrix from the configuration, runs the tests as per the matrix,
    and saves the results to a CSV file.
    """

    config_file = "loadtest/test_config.json"
    test_matrix = construct_test_matrix(config_file)
    final_matrix = (
        test_matrix
        if design_type == "full"
        else fractional_design(test_matrix, fraction)
    )

    results = []
    load_tester = LoadTester()

    for endpoint, request_type, payload_size, concurrency in final_matrix:
        duration, creations, failures = load_tester.run_test(
            endpoint, request_type, payload_size, concurrency
        )
        results.append(
            [
                endpoint,
                request_type,
                payload_size,
                concurrency,
                duration,
                creations,
                failures,
            ]
        )

    # Ensure the data directory exists
    data_dir = "loadtest/data"
    os.makedirs(data_dir, exist_ok=True)

    # Create a timestamped filename for the results
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(data_dir, f"results_{timestamp}.csv")

    # Save the results to the CSV file
    save_results_to_csv(results, filename)


if __name__ == "__main__":
    app()
