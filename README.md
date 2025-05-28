Bulk Certificate Checker

    Bulk SSL/TLS certificate expiration checker

Checks certificate expiry dates for multiple domains in parallel and generates a CSV report.
🚀 Features

    Fast bulk checking of SSL/TLS certificates

    CSV output with hostname, expiry date, days left, and status

    Flags certificates expiring soon or errors

    Easy CI/CD integration with GitHub Actions

📋 Table of Contents

    Prerequisites

    Installation

    Usage

    Examples

    Configuration

    CI/CD Integration

    Tests

    Contributing

    License

📋 Prerequisites

    Python 3.7 or higher

    Internet access to target hosts (port 443)

🔧 Installation
git clone https://github.com/MarcMontolio/bulk-certificate-checker.git
cd bulk-certificate-checker
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\Activate.ps1    # Windows PowerShell
pip install --upgrade pip
pip install -r requirements.txt
▶️ Usage

Run the script with input and output paths:
python src/check_certs.py \
  --input examples/sample_input.txt \
  --output report.csv \
  --warn 30

Options:

    -i, --input: Path to a text file (one hostname per line)

    -o, --output: Path to CSV report (default: report.csv)

    -w, --warn: Days before expiry to flag (default: 30)

🔍 Examples

Example input (examples/sample_input.txt):
example.com
expired.badssl.com
google.com

Example output (examples/sample_report.csv):
hostname,expiry_date,days_left,status
example.com,2026-01-15T23:59:59,232,OK
expired.badssl.com,,,ERROR: certificate verify failed: certificate has expired
google.com,2025-07-22T19:28:09,54,OK
⚙️ Configuration

    Change the default warning threshold (warn_days) in the CLI options.

    To check non-standard ports, modify get_cert_expiry() in src/check_certs.py.

⚙️ CI/CD Integration

The included GitHub Actions workflow (.github/workflows/ci.yml) does the following:

    Lints with flake8

    Runs tests via pytest

To fail a pipeline if certs are near expiry:
- name: Check SSL certificates
  run: |
    python src/check_certs.py -i examples/sample_input.txt -o report.csv -w 7
    if grep -q EXPIRES_SOON report.csv; then
      echo "Certificate expiry warning detected!" >&2
      exit 1
    fi
🧪 Tests

Run all tests using:
pytest -q
🤝 Contributing

Contributions are welcome! To get started:

    Fork the repo

    Create a feature branch

    Run the test suite locally (pytest)

    Submit a pull request

📜 License

MIT License © 2025 Marc Montolio


