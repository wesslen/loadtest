import requests
import time
import threading
import numpy as np
from rich.console import Console
from rich.table import Table
import typer
from .constants import TEST_URL, BASE_URL

app = typer.Typer()


class HTTPBenchmark:
    def __init__(
        self,
        base_url,
        url,
        num_requests,
        method="GET",
        data=None,
        headers=None,
        concurrency=1,
    ):
        self.base_url = base_url
        self.url = url
        self.num_requests = num_requests
        self.method = method
        self.data = data
        self.headers = headers
        self.concurrency = concurrency
        self.latencies = []
        self.errors = 0

    def _make_request(self):
        try:
            start_time = time.time()
            if self.method == "GET":
                response = requests.get(
                    f"{self.base_url}/{self.url}", headers=self.headers
                )
            elif self.method == "POST":
                response = requests.post(
                    f"{self.base_url}/{self.url}", data=self.data, headers=self.headers
                )
            end_time = time.time()
            self.latencies.append(end_time - start_time)
        except requests.RequestException:
            self.errors += 1

    def _worker(self):
        for _ in range(int(self.num_requests / self.concurrency)):
            self._make_request()

    def display_results(self):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="dim", width=20)
        table.add_column("Value")
        table.add_row("BASE_URL", self.base_url)
        table.add_row("URL", self.url)
        table.add_row("Total Requests", str(self.num_requests))
        table.add_row("Failed Requests", str(self.errors))
        table.add_row(
            "Median Latency", f"{np.percentile(self.latencies, 50):.4f} seconds"
        )
        table.add_row("75% Latency", f"{np.percentile(self.latencies, 75):.4f} seconds")
        table.add_row("95% Latency", f"{np.percentile(self.latencies, 95):.4f} seconds")
        table.add_row("99% Latency", f"{np.percentile(self.latencies, 99):.4f} seconds")
        console.print(table)

    def run(self):
        threads = []
        for _ in range(self.concurrency):
            thread = threading.Thread(target=self._worker)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.display_results()


@app.command()
def main(
    base_url: str = typer.Option(BASE_URL, help="The Base URL to benchmark."),
    url: str = typer.Option(TEST_URL, help="The URL to benchmark."),
    num_requests: int = typer.Option(100, help="Total number of requests to perform."),
    method: str = typer.Option("GET", help="HTTP method to use."),
    concurrency: int = typer.Option(1, help="Number of concurrent requests."),
):
    """
    Executes a simple HTTP benchmarking tool that performs a specified number of HTTP requests to a given URL,
    displays the results including various latency metrics, and handles concurrent requests.
    """
    benchmark = HTTPBenchmark(
        base_url=base_url,
        url=url,
        num_requests=num_requests,
        method=method,
        concurrency=concurrency,
    )
    benchmark.run()


if __name__ == "__main__":
    app()
