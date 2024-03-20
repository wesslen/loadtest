import requests
import time
import typer

app = typer.Typer()


class LoadTester:
    def __init__(self):
        # Initialize any necessary attributes here (e.g., for logging or storing results)
        pass

    def run_test(self, endpoint, request_type, payload_size, concurrency):
        # Simulate payload - In a real scenario, this should be meaningful data
        payload = "x" * payload_size

        # Record start time
        start_time = time.time()

        # Initialize counters for successful creations and failures
        creations = 0
        failures = 0

        # Execute the request based on the type
        if request_type == "GET":
            for _ in range(concurrency):
                response = requests.get(endpoint)
                if response.status_code != 200:
                    failures += 1
                    print(f"Request failed with status code: {response.status_code}")
        elif request_type == "POST":
            for _ in range(concurrency):
                response = requests.post(endpoint, data=payload)
                if response.status_code == 201:
                    creations += 1
                else:
                    failures += 1
                    print(f"Request failed with status code: {response.status_code}")

        # Record end time and calculate the duration
        end_time = time.time()
        duration = end_time - start_time

        # Output the result
        print(
            f"Executed {concurrency} {request_type} requests to {endpoint} with payload size {payload_size} bytes in {duration:.2f} seconds."
        )
        if creations:
            print(f"{creations} requests resulted in new resource creations.")
        if failures:
            print(f"{failures} requests failed.")

        # Return the duration, number of creations, and number of failures
        return duration, creations, failures


@app.command()
def run(
    endpoint: str = typer.Option(
        ..., help="The endpoint URL to target with the load test."
    ),
    request_type: str = typer.Option(
        ..., help="The type of HTTP request to perform ('GET' or 'POST')."
    ),
    payload_size: int = typer.Option(
        0, help="The size of the payload for POST requests, in bytes."
    ),
    concurrency: int = typer.Option(
        1, help="The number of concurrent requests to make."
    ),
):
    """
    Executes a load test on a specified endpoint using a specified number of concurrent requests of a given type and,
    for POST requests, a specified payload size. The function reports on the success and failure of the requests and
    provides a summary of the test's execution time.
    """
    tester = LoadTester()
    tester.run_test(endpoint, request_type, payload_size, concurrency)


if __name__ == "__main__":
    app()
