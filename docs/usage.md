🧪 Usage Guide – Bulk Certificate Checker

A short, focused guide on how to run the bulk-certificate-checker tool, with just enough detail to get things done efficiently.

📦 Requirements

Python 3.7+

Internet access to the domains you're checking (port 443)

A terminal and a will to type things

🚀 Setup

Clone the project:

git clone https://github.com/MarcMontolio/bulk-certificate-checker.git
cd bulk-certificate-checker

(Recommended) Set up a virtual environment:

python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\Activate.ps1     # Windows PowerShell

Install the required packages:

pip install --upgrade pip
pip install -r requirements.txt

🏃 Running the Script

Basic command:

python src/check_certs.py \
  --input examples/sample_input.txt \
  --output examples/sample_report.csv

CLI Options:

--input, -i: Path to a text file with one hostname per line

--output, -o: Output CSV path (default: report.csv)

--warn, -w: Days before expiry to flag as EXPIRES_SOON (default: 30)

🧾 Example

Sample input file examples/sample_input.txt:

example.com
expired.badssl.com
google.com

Run:

python src/check_certs.py -i examples/sample_input.txt -o examples/sample_report.csv -w 15

Sample output (sample_report.csv):

hostname,expiry_date,days_left,status
example.com,2026-01-15T23:59:59,232,OK
expired.badssl.com,,,ERROR: certificate verify failed: certificate has expired
google.com,2025-07-22T19:28:09,54,OK

⚙️ Advanced Usage

Custom Port

Want to check a port that isn't 443? Edit the get_cert_expiry() function inside src/check_certs.py.

CI/CD Integration

Use it in GitHub Actions to fail builds when certs are close to expiring:

- name: Check SSL certificates
  run: |
    python src/check_certs.py -i examples/sample_input.txt -o report.csv -w 7
    if grep -q EXPIRES_SOON report.csv; then
      echo "One or more certificates will expire soon!" >&2
      exit 1
    fi

Error Reporting

If a host fails validation or is unreachable, the status column will report ERROR: <details>

Exit code is always 0; your CI must parse the CSV to detect issues

📁 Project Structure

bulk-certificate-checker/
├─ .github/
│  └─ workflows/ci.yml
├─ docs/
│  └─ usage.md
├─ examples/
│  ├─ sample_input.txt
│  └─ sample_report.csv
├─ src/
│  ├─ __init__.py
│  └─ check_certs.py
├─ tests/
│  ├─ conftest.py
│  └─ test_check_certs.py
├─ .gitignore
├─ requirements.txt
└─ README.md

🙌 Contributing

Fork the project

Create a new branch

Write your code + tests (pytest)

Open a Pull Request

📄 License

MIT License © 2025 Marc Montolio

