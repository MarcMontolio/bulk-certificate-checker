#!/usr/bin/env python3
"""
ssl-checker.py

Mass-check SSL/TLS certificate expiry dates from a list of hostnames.
Outputs a CSV with hostname, expiry date, days left, and a status field.
Good for people who don't trust expiration emails or joy.
"""

import csv
import socket
import ssl
from datetime import datetime, timedelta
import click


def get_cert_expiry(hostname: str, port: int = 443, timeout: int = 5) -> datetime:
    """
    Grab the SSL/TLS certificate's expiry date from a given hostname.

    Args:
        hostname (str): The domain or IP to connect to.
        port (int): Port to use. Default is 443, obviously.
        timeout (int): How long to wait before giving up. In seconds.

    Returns:
        datetime: The 'notAfter' field parsed into a datetime object.

    Raises:
        socket.error, ssl.SSLError: When things go sideways.
    """
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port), timeout=timeout) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expiry_str = cert.get('notAfter')
            return datetime.strptime(expiry_str, '%b %d %H:%M:%S %Y %Z')


@click.command()
@click.option(
    '-i', '--input', 'infile', required=True,
    help='Path to input file with hostnames (one per line).'
)
@click.option(
    '-o', '--output', 'outfile', default='report.csv', show_default=True,
    help='Where to write the CSV output.'
)
@click.option(
    '-w', '--warn', 'warn_days', default=30, show_default=True,
    help='Threshold (in days) to flag as EXPIRES_SOON.'
)
def main(infile: str, outfile: str, warn_days: int):
    """
    Reads hostnames from file, checks SSL cert expiry dates,
    and writes results to CSV with days remaining and status.

    Status values:
        - 'OK': Certificate is fine.
        - 'EXPIRES_SOON': Panic might be required.
        - 'ERROR: <message>': Something went wrong.
    """
    warn_delta = timedelta(days=warn_days)

    with open(infile, 'r') as f, open(outfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['hostname', 'expiry_date', 'days_left', 'status'])

        for line in f:
            host = line.strip()
            if not host:
                continue  # No hostname, no cry.

            try:
                exp = get_cert_expiry(host)
                days_left = (exp - datetime.utcnow()).days
                status = 'OK' if days_left > warn_days else 'EXPIRES_SOON'
                writer.writerow([host, exp.isoformat(), days_left, status])
            except Exception as e:
                writer.writerow([host, '', '', f'ERROR: {e}'])


if __name__ == '__main__':
    main()
