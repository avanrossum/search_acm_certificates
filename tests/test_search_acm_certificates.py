import sys
from pathlib import Path
import pytest
from unittest.mock import MagicMock, patch

sys.path.append(str(Path(__file__).resolve().parent.parent))
from search_acm_certificates import search_acm_certificates, display_results


class MockPaginator:
    def __init__(self, pages):
        self.pages = pages

    def paginate(self):
        for page in self.pages:
            yield page


def test_search_acm_certificates_returns_matching_certificate():
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = MockPaginator([
        {
            "CertificateSummaryList": [
                {"CertificateArn": "arn:aws:acm:us-east-1:123456789012:certificate/1"},
                {"CertificateArn": "arn:aws:acm:us-east-1:123456789012:certificate/2"},
            ]
        }
    ])

    def describe_side_effect(CertificateArn):
        if CertificateArn.endswith("/1"):
            return {
                "Certificate": {
                    "DomainName": "example.com",
                    "SubjectAlternativeNames": ["example.com", "www.example.com"],
                    "Status": "ISSUED",
                    "NotBefore": "NB",
                    "NotAfter": "NA",
                    "Issuer": "Amazon",
                    "Subject": "CN=example.com",
                }
            }
        else:
            return {
                "Certificate": {
                    "DomainName": "other.com",
                    "SubjectAlternativeNames": ["other.com"],
                    "Status": "ISSUED",
                    "NotBefore": "NB",
                    "NotAfter": "NA",
                    "Issuer": "Amazon",
                    "Subject": "CN=other.com",
                }
            }

    mock_client.describe_certificate.side_effect = describe_side_effect

    with patch("search_acm_certificates.boto3.client", return_value=mock_client):
        results = search_acm_certificates("example.com")

    assert len(results) == 1
    cert = results[0]
    assert cert["domain_name"] == "example.com"
    assert cert["found_in_domains"] is True


def test_search_acm_certificates_no_matches():
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = MockPaginator([
        {
            "CertificateSummaryList": [
                {"CertificateArn": "arn:aws:acm:us-east-1:123456789012:certificate/1"},
            ]
        }
    ])
    mock_client.describe_certificate.return_value = {
        "Certificate": {
            "DomainName": "other.com",
            "SubjectAlternativeNames": ["other.com"],
            "Status": "ISSUED",
            "NotBefore": "NB",
            "NotAfter": "NA",
            "Issuer": "Amazon",
            "Subject": "CN=other.com",
        }
    }

    with patch("search_acm_certificates.boto3.client", return_value=mock_client):
        results = search_acm_certificates("example.com")

    assert results == []


def test_display_results_outputs_matches(capsys):
    certificates = [
        {
            "arn": "arn:aws:acm:us-east-1:123456789012:certificate/1",
            "domain_name": "example.com",
            "subject_alternative_names": ["example.com", "www.example.com"],
            "status": "ISSUED",
            "not_before": "NB",
            "not_after": "NA",
            "issuer": "Amazon",
            "found_in_domains": True,
            "found_in_subject": False,
        }
    ]

    display_results(certificates, "example.com")
    captured = capsys.readouterr()
    assert "Found 1 certificate(s)" in captured.out
    assert "example.com" in captured.out
