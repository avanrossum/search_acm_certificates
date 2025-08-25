# AWS ACM Certificate Search Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/avanrossum/search_acm_certificates/actions/workflows/tests.yml/badge.svg)](https://github.com/avanrossum/search_acm_certificates/actions/workflows/tests.yml)

A Python script to search AWS Certificate Manager (ACM) for certificates containing specific domain strings. This tool helps you quickly find certificates that match your domain criteria, whether you're looking for exact matches or partial domain matches.

## Features

- **Flexible Search**: Search for exact domain matches or partial domain strings
- **Comprehensive Results**: Shows certificate ARN, domain names, status, validity dates, and issuer
- **Multi-Region Support**: Search in specific AWS regions or use your default region
- **Subject Alternative Names**: Searches through all SANs (Subject Alternative Names) in addition to the main domain
- **Visual Indicators**: Matching domains are highlighted in green with checkmarks
- **Pagination Support**: Efficiently handles large numbers of certificates
- **Error Handling**: Graceful error handling for connection and access issues

## Prerequisites

- Python 3.6 or higher
- AWS CLI configured with appropriate credentials
- Required permissions to list and describe ACM certificates

### Required AWS Permissions

Your AWS credentials need the following permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "acm:ListCertificates",
                "acm:DescribeCertificate"
            ],
            "Resource": "*"
        }
    ]
}
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/search_acm_certificates.git
   cd search_acm_certificates
   ```

2. **Install dependencies**:
   ```bash
   pip install boto3
   ```

3. **Configure AWS credentials** (if not already configured):
   ```bash
   aws configure
   ```

## Usage

### Basic Usage

Search for certificates containing a specific domain:

```bash
python search_acm_certificates.py example.com
```

### Advanced Usage

Search for wildcard certificates:
```bash
python search_acm_certificates.py "*.example.com"
```

Search in a specific AWS region:
```bash
python search_acm_certificates.py api --region us-east-1
```

Search with verbose output:
```bash
python search_acm_certificates.py mydomain.com --verbose
```

### Command Line Options

- `domain_search`: The domain string to search for (supports partial matches)
- `--region`: AWS region (defaults to your default region)
- `--verbose, -v`: Enable verbose output

## Examples

### Example 1: Search for a specific domain
```bash
python search_acm_certificates.py api.example.com
```

**Output:**
```
Searching for certificates containing: 'api.example.com'
------------------------------------------------------------

Found 1 certificate(s) containing 'api.example.com':
================================================================================

Certificate 1:
  ARN: arn:aws:acm:us-east-1:123456789012:certificate/abcd1234-5678-90ef-ghij-klmnopqrstuv
  Domain Name: api.example.com
  Status: ISSUED
  Subject Alternative Names:
    - api.example.com ✓
    - *.api.example.com ✓
  Valid From: 2023-01-15 00:00:00+00:00
  Valid Until: 2024-01-15 23:59:59+00:00
  Issuer: C=US, O=Amazon, OU=Server CA 1B, CN=Amazon
----------------------------------------
```

### Example 2: Search for partial domain matches
```bash
python search_acm_certificates.py api
```

This will find all certificates containing "api" in any domain name or SAN.

### Example 3: Search for wildcard certificates
```bash
python search_acm_certificates.py "*.example.com"
```

## Output Format

The script provides detailed information for each matching certificate:

- **ARN**: The AWS Resource Name of the certificate
- **Domain Name**: The primary domain name
- **Status**: Certificate status (ISSUED, PENDING_VALIDATION, etc.)
- **Subject Alternative Names**: All additional domains covered by the certificate
- **Valid From/Until**: Certificate validity period
- **Issuer**: Certificate authority information

Matching domains are highlighted in **green** with a checkmark (✓) for easy identification.

## Troubleshooting

### Common Issues

1. **AWS Credentials Not Configured**
   ```
   Error connecting to AWS ACM: Unable to locate credentials
   ```
   **Solution**: Run `aws configure` to set up your credentials

2. **Insufficient Permissions**
   ```
   Error getting details for certificate: AccessDenied
   ```
   **Solution**: Ensure your AWS user/role has the required ACM permissions

3. **Region Issues**
   ```
   Error connecting to AWS ACM: NoRegionError
   ```
   **Solution**: Specify a region with `--region` or set a default region in AWS config

4. **No Certificates Found**
   - Verify you're searching in the correct AWS region
   - Check that your search string is correct
   - Ensure you have access to the certificates in that region

### Debug Mode

Use the `--verbose` flag to get more detailed output about the search process:

```bash
python search_acm_certificates.py example.com --verbose
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security

- This script only reads certificate information and does not modify any AWS resources
- Ensure your AWS credentials are properly secured
- Consider using IAM roles with minimal required permissions
- Never commit AWS credentials to version control

## Support

If you encounter any issues or have questions, please:

1. Check the troubleshooting section above
2. Search existing issues in the repository
3. Create a new issue with detailed information about your problem

## Changelog

### Version 1.0.0
- Initial release
- Basic domain search functionality
- Support for partial matches
- Multi-region support
- Visual indicators for matches
