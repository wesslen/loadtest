import json
from unittest.mock import mock_open, patch
from tests import run_tests

def test_construct_test_matrix():
    # Mock data to simulate the content of config_file
    mock_data = {
        "endpoints": ["endpoint1", "endpoint2"],
        "request_types": ["GET", "POST"],
        "payload_sizes": [100, 200],
        "concurrency_levels": [1, 2]
    }
    expected_matrix = list(run_tests.itertools.product(
        mock_data['endpoints'],
        mock_data['request_types'],
        mock_data['payload_sizes'],
        mock_data['concurrency_levels']
    ))

    # Use mock_open to mock the open function within construct_test_matrix
    with patch("tests.run_tests.open", mock_open(read_data=json.dumps(mock_data))) as mocked_file:
        # Call the function under test
        result_matrix = run_tests.construct_test_matrix("dummy_config_file")

        # Assert the result is as expected
        assert result_matrix == expected_matrix, "The generated test matrix does not match the expected matrix."

# This is for making the test module executable, useful for debugging
if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
