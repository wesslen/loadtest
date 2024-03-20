from unittest.mock import patch, MagicMock, call
from loadtest.__main__ import HTTPBenchmark
import requests

def test_httpbenchmark_initialization():
    """
    Test the initialization of the HTTPBenchmark class.
    """
    base_url = "http://example.com/"
    url = "posts"
    num_requests = 10
    method = "POST"
    data = {"key": "value"}
    headers = {"Content-Type": "application/json"}
    concurrency = 2

    benchmark = HTTPBenchmark(
        base_url=base_url,
        url=url,
        num_requests=num_requests,
        method=method,
        data=data,
        headers=headers,
        concurrency=concurrency
    )

    assert benchmark.base_url == base_url
    assert benchmark.url == url
    assert benchmark.num_requests == num_requests
    assert benchmark.method == method
    assert benchmark.data == data
    assert benchmark.headers == headers
    assert benchmark.concurrency == concurrency
    assert benchmark.latencies == []
    assert benchmark.errors == 0

def test_make_request_get_success():
    """
    Test the _make_request method for a successful GET request.
    """
    with patch('loadtest.__main__.requests.get') as mock_get:
        # Mock the response to simulate a successful GET request.
        mock_response = MagicMock()
        mock_response.elapsed = MagicMock()
        mock_response.elapsed.total_seconds.return_value = 0.1
        mock_get.return_value = mock_response

        benchmark = HTTPBenchmark(base_url="http://example.com/", url="posts", num_requests=1)
        benchmark._make_request()

        # Ensure a latency was recorded and is greater than zero, and no errors were incremented.
        assert len(benchmark.latencies) == 1
        assert benchmark.latencies[0] > 0
        assert benchmark.errors == 0

def test_make_request_with_exception():
    """
    Test the _make_request method when an exception is raised (simulating a failed request).
    """
    with patch('loadtest.__main__.requests.get') as mock_get:
        # Simulate a request exception
        mock_get.side_effect = requests.RequestException

        benchmark = HTTPBenchmark(base_url="http://example.com/", url="posts", num_requests=1)
        benchmark._make_request()

        # Ensure no latency was recorded and an error was incremented.
        assert len(benchmark.latencies) == 0
        assert benchmark.errors == 1


def test_run_method_with_concurrency():
    """
    Test the run method with concurrency, ensuring multiple threads are used to make requests.
    """
    num_requests = 4
    concurrency = 2

    with patch('loadtest.__main__.threading.Thread') as mock_thread:
        # Mock the Thread class to prevent actual threading
        mock_thread.side_effect = lambda *args, **kwargs: MagicMock(start=MagicMock(), join=MagicMock())

        with patch('loadtest.__main__.HTTPBenchmark._make_request'):
            benchmark = HTTPBenchmark(base_url="http://example.com/", url="posts", num_requests=num_requests, concurrency=concurrency)

            with patch('loadtest.__main__.HTTPBenchmark.display_results'):
                benchmark.run()

                # Check if the correct number of threads were started
                assert mock_thread.call_count == concurrency
                
                # Ensure that the target for each thread is the _worker method
                for call_args in mock_thread.call_args_list:
                    args, kwargs = call_args
                    assert kwargs['target'] == benchmark._worker