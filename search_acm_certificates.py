#!/usr/bin/env python3
"""
AWS ACM Certificate Search Script

This script searches AWS ACM for certificates that contain a specific domain string.
It supports both exact matches and partial matches for domain names.
"""

import boto3
import argparse
import sys
from datetime import datetime
from typing import List, Dict, Any


def search_acm_certificates(domain_search: str, region: str = None) -> List[Dict[str, Any]]:
    """
    Search ACM certificates for certificates containing the specified domain string.
    
    Args:
        domain_search (str): The domain string to search for
        region (str): AWS region (optional, uses default if not specified)
    
    Returns:
        List[Dict]: List of matching certificates with their details
    """
    try:
        # Initialize ACM client
        if region:
            acm_client = boto3.client('acm', region_name=region)
        else:
            acm_client = boto3.client('acm')
        
        # Get all certificates
        paginator = acm_client.get_paginator('list_certificates')
        matching_certificates = []
        
        print(f"Searching for certificates containing: '{domain_search}'")
        print("-" * 60)
        
        for page in paginator.paginate():
            for cert in page['CertificateSummaryList']:
                cert_arn = cert['CertificateArn']
                
                # Get detailed certificate information
                try:
                    cert_details = acm_client.describe_certificate(CertificateArn=cert_arn)
                    certificate = cert_details['Certificate']
                    
                    # Check if the domain search string is in any of the domain names
                    domain_names = certificate.get('SubjectAlternativeNames', [])
                    subject = certificate.get('Subject', '')
                    
                    # Search in domain names and subject
                    found_in_domains = any(domain_search.lower() in domain.lower() for domain in domain_names)
                    found_in_subject = domain_search.lower() in str(subject).lower()
                    
                    if found_in_domains or found_in_subject:
                        matching_certificates.append({
                            'arn': cert_arn,
                            'domain_name': certificate.get('DomainName', 'N/A'),
                            'subject_alternative_names': domain_names,
                            'status': certificate.get('Status', 'N/A'),
                            'not_before': certificate.get('NotBefore', 'N/A'),
                            'not_after': certificate.get('NotAfter', 'N/A'),
                            'issuer': certificate.get('Issuer', 'N/A'),
                            'found_in_domains': found_in_domains,
                            'found_in_subject': found_in_subject
                        })
                        
                except Exception as e:
                    print(f"Error getting details for certificate {cert_arn}: {e}")
                    continue
        
        return matching_certificates
        
    except Exception as e:
        print(f"Error connecting to AWS ACM: {e}")
        return []


def display_results(certificates: List[Dict[str, Any]], domain_search: str):
    """
    Display the search results in a formatted way.
    
    Args:
        certificates (List[Dict]): List of matching certificates
        domain_search (str): The original search string
    """
    if not certificates:
        print(f"No certificates found containing '{domain_search}'")
        return
    
    print(f"\nFound {len(certificates)} certificate(s) containing '{domain_search}':")
    print("=" * 80)
    
    for i, cert in enumerate(certificates, 1):
        print(f"\nCertificate {i}:")
        print(f"  ARN: {cert['arn']}")
        print(f"  Domain Name: {cert['domain_name']}")
        print(f"  Status: {cert['status']}")
        
        if cert['subject_alternative_names']:
            print(f"  Subject Alternative Names:")
            for san in cert['subject_alternative_names']:
                if domain_search.lower() in san.lower():
                    print(f"    - \033[92m{san} ✓\033[0m")  # Green color for matches
                else:
                    print(f"    - {san}")
        
        if cert['not_before'] != 'N/A':
            print(f"  Valid From: {cert['not_before']}")
        if cert['not_after'] != 'N/A':
            print(f"  Valid Until: {cert['not_after']}")
        
        if cert['issuer'] != 'N/A':
            print(f"  Issuer: {cert['issuer']}")
        
        print("-" * 40)


def main():
    """Main function to handle command line arguments and execute the search."""
    parser = argparse.ArgumentParser(
        description='Search AWS ACM certificates for a specific domain string',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python find_acm_certificate.py example.com
  python find_acm_certificate.py "*.example.com" --region us-east-1
  python find_acm_certificate.py api --region eu-west-1
        """
    )
    
    parser.add_argument(
        'domain_search',
        help='Domain string to search for (supports partial matches)'
    )
    
    parser.add_argument(
        '--region',
        help='AWS region (defaults to your default region)',
        default=None
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Searching in region: {args.region or 'default'}")
    
    # Perform the search
    certificates = search_acm_certificates(args.domain_search, args.region)
    
    # Display results
    display_results(certificates, args.domain_search)
    
    if certificates:
        print(f"\nSearch completed. Found {len(certificates)} matching certificate(s).")
    else:
        print(f"\nSearch completed. No certificates found containing '{args.domain_search}'.")


if __name__ == "__main__":
    main()
