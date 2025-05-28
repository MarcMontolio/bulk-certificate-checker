import csv
from datetime import datetime, timedelta
import pytest
from click.testing import CliRunner

# Import the module so monkeypatching works on its attributes
import src.check_certs as check_certs_module


def test_get_cert_expiry_monkeypatched(monkeypatch):
    """Ensure get_cert_expiry returns the expected datetime when patched."""

    mock_expiry = datetime(2030, 1, 1)

    def mock_get(*args, **kwargs):
        return mock_expiry

    # Patch the function on the module object
    monkeypatch.setattr(check_certs_module, "get_cert_expiry", mock_get)

    # Call via the module so the patch is applied
    assert check_certs_module.get_cert_expiry("example.com") == mock_expiry


def test_cli_output(tmp_path, monkeypatch):
    """Validate CLI output with mocked certificate data."""

    base_date = datetime(2030, 1, 1)

    def mock_get(hostname, *args, **kwargs):
        return base_date + timedelta(days=10)

    # Patch the function used by the CLI
    monkeypatch.setattr(check_certs_module, "get_cert_expiry", mock_get)

    # Prepare input file
    input_file = tmp_path / "hosts.txt"
    input_file.write_text("host1.com\nhost2.net\n")

    output_file = tmp_path / "out.csv"

    # Invoke the CLI entrypoint from the module
    runner = CliRunner()
    result = runner.invoke(check_certs_module.main, [
        "-i", str(input_file),
        "-o", str(output_file),
        "-w", "5"
    ])
    assert result.exit_code == 0

    # Read and verify CSV contents
    with output_file.open() as f:
        rows = list(csv.reader(f))

    assert rows[0] == ["hostname", "expiry_date", "days_left", "status"]
    assert rows[1][0] == "host1.com" and rows[1][3] == "OK"
    assert rows[2][0] == "host2.net" and rows[2][3] == "OK"
