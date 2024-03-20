# CLI Reference

This page provides documentation for the command line tools.

## `loadtest`

Executes a simple HTTP benchmarking tool that performs a specified number of HTTP requests to a given URL,
displays the results including various latency metrics, and handles concurrent requests.

This tool allows users to specify the target URL, the total number of requests, the HTTP method (GET or POST), and
the level of concurrency for the requests. It provides a detailed report on the performance of the HTTP requests,
including metrics such as median, 75th percentile, 95th percentile, and 99th percentile latencies.

Parameters:

- url (str): The URL to be benchmarked. This is the target endpoint where the HTTP requests will be sent.
- num_requests (int): The total number of HTTP requests to perform against the target URL. This defines the load
    intensity of the benchmark.
- method (str): The HTTP method to use for the requests. This can be either 'GET' or 'POST'. The default method is
    'GET'.
- concurrency (int): The number of concurrent requests to make. This parameter allows the benchmark to simulate
    multiple users or processes making requests to the same endpoint simultaneously.

The benchmark will output a table showing the URL tested, the total number of requests made, the number of failed
requests, and latency statistics (median, 75%, 95%, and 99% latencies) to provide a comprehensive view of the
endpoint's performance under the specified load.

Example usage:
```shell
python -m loadtest --url http://example.com --num_requests 100 --method GET --concurrency 10
```

This command will benchmark the specified URL using 100 GET requests with 10 concurrent requests.

Note: The tool requires an internet connection to perform the HTTP requests and the URL provided should be accessible
from the host machine where the script is run.

## `loadtest.load_tester`

Executes a load test on a specified endpoint using a specified number of concurrent requests of a given type and,
for POST requests, a specified payload size. The function reports on the success and failure of the requests and
provides a summary of the test's execution time.

Parameters:

- endpoint (str): The target URL for the load testing. This should be a valid HTTP or HTTPS endpoint where the load
    test will send the requests.
- request_type (str): Specifies the type of HTTP request to perform. Valid options are 'GET' or 'POST'. This
    determines the HTTP method used to interact with the endpoint.
- payload_size (int): Defines the size of the payload in bytes for POST requests. This is ignored for GET requests.
    The payload is a string of repeated 'x' characters of the specified size.
- concurrency (int): The number of requests to send concurrently. This simulates multiple users or systems
    interacting with the endpoint simultaneously and can help assess the endpoint's capacity to handle multiple
    requests.

The function performs the load test by sending the specified number of concurrent requests to the endpoint. For POST
requests, it sends a payload of the specified size with each request. The function counts the number of successful
requests and failures and prints a summary of the test results, including the total duration of the test, the number
of successful creations (for POST requests), and the number of failures.

Example usage:
```shell
python -m loadtest.load_tester --endpoint http://example.com/api --request_type POST --payload_size 500 --concurrency 10
```

This command will send 10 concurrent POST requests to the specified endpoint, each with a payload of 500 bytes.

Note: This script is intended for load testing purposes and should be used responsibly. Ensure that you have
permission to perform load testing on the target endpoint and that the test will not negatively impact the endpoint
or its network.

Returns:

- duration (float): The total time taken to execute all the requests in seconds.
- creations (int): The number of successful resource creations (relevant for POST requests).
- failures (int): The number of requests that resulted in failure (e.g., due to server errors or timeouts).


## `tests.run_tests`

Executes a series of load tests based on configurations defined in a JSON file, allowing for either full or
fractional testing. The script generates a test matrix from the configuration, runs the tests as per the matrix,
and saves the results to a CSV file.

The test matrix is constructed from a combination of endpoints, request types, payload sizes, and concurrency levels
specified in the configuration file. Users can choose to run all possible combinations (full) or a random fraction
of these combinations (fractional).

Parameters:

- design_type (str): Specifies the type of test matrix design to use. It can be 'full' for testing all combinations
    or 'fractional' for testing a fraction of all combinations.
- fraction (float): Specifies the fraction of the test matrix to execute. This is required if design_type is
    'fractional'. For example, a fraction of 0.5 means that half of the total combinations will be randomly selected
    and tested.

The script performs the following steps:

1. Constructs the test matrix from the configuration file.
2. Depending on the design_type, it either uses the full matrix or selects a fraction of the combinations.
3. Executes the load tests for each combination in the final test matrix using the LoadTester class.
4. Collects the results from each test, including the duration, number of creations, and number of failures.
5. Saves the results in a CSV file with a timestamp in the filename to ensure uniqueness.

Results are saved in the 'tests/data' directory with filenames following the 'results_YYYYMMDD_HHMMSS.csv' format.

Example usage:
```shell
python -m tests.run_tests --design_type fractional --fraction 0.5
```

This command will execute a load test using a fractional design, testing only half of the possible combinations
defined in the test configuration file.

Note: This script assumes the presence of a JSON configuration file ('tests/test_config.json') and relies on the
`LoadTester` class for executing the load tests.

## `tests.visualize_results`

Launches a Streamlit app to visualize load test results from CSV files stored in a specified directory.

The app provides interactive controls to select a results file, endpoint, request type, and metric for
visualization. It displays a line chart and a detailed data table based on the selections.

Parameter:

- data_dir (str): Path to the directory containing the CSV files with load test results. By default it is `tests/data`

The Streamlit app includes:

- A dropdown to select a results file from the specified directory.
- A dropdown to select an endpoint from the available options in the selected file.
- Dropdowns to select the type of request and the metric (Duration or Failures) to display on the y-axis of the chart.
- An Altair line chart visualizing the selected metric over concurrency levels, colored by payload sizes.
- A data table displaying the detailed data for the selected filters.

To run the app, execute the command: `python -m streamlit run tests/visualize_results.py --data-dir <path_to_data_dir>`