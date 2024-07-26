# !/usr/bin/env python

import requests
import json
from .constants import Constants, HttpMethods
from .base_connector_class import BaseConnectorClass

"""
NVD Connector
Connector Category : IT Services
Supported Version : 1.0.0
Connector Description : The National Vulnerability Database is the U.S. government repository of standards-based vulnerability management data represented using the Security Content Automation Protocol. This data enables automation of vulnerability management, security measurement, and compliance.
Authentication supported: API Key
Connector Version: 1.0.0
Documentation URL: 
Release Notes: 
"""


class NvdConnector(object):
    def __init__(self, api_key: str,
                 **kwargs):
        """
        :param api_key: Enter the API credentials from NVD. An API key can be requested at https://nvd.nist.gov/developers/request-an-api-key
        """
        self.api_key = api_key
        self.base_url = "https://services.nvd.nist.gov/rest/json"

    def test_connection(self, **kwargs):
        url = f"{self.base_url}/cves/2.0/"
        headers = {
            "apiKey": self.api_key
        }
        response = BaseConnectorClass().test_connection(method=HttpMethods.GET.value, url=url,
                                                    headers=headers)
        return response

    def action_list_cves(self, severity: str = None, cwe_id: str = None, keyword: str = None,
                         published_start_date: str = None,
                         published_end_date: str = None, page_size: int = None, start_index: int = None,
                         extra_params: dict = None, **kwargs):
        """
        This action is used to list all CVE's from NVD
        :param severity: Enter the severity to filter vulnerabilities by. Allowed values are: LOW, MEDIUM, HIGH, or CRITICAL
        :param cwe_id: Enter a CWE to search by
        :param keyword: Enter a keyword to search by
        :param published_start_date: Enter the datetime string to filter vulnerabilities added after. This should be in the format - yyyy-MM-ddTHH:mm:ss:SSS Z. If we are filtering by date, both start and end dates have to be specified
        :param published_end_date: Enter the datetime string to filter vulnerabilities added before. This should be in the format - yyyy-MM-ddTHH:mm:ss:SSS Z. If we are filtering by date, both start and end dates have to be specified
        :param page_size: Enter the number of responses to return. This defaults to 20. Max allowed number is 2000
        :param start_index: Enter the start index to get responses from. This defaults to 0.
        :param extra_params: Enter any extra params to pass along with this request. Eg: modStartDate, modEndDate
        """
        if published_start_date or published_end_date:
            if not published_start_date and published_end_date:
                return {
                    Constants.ACTION_STATUS: Constants.ERROR,
                    Constants.ACTION_RESULT: "To filter by date, both start and end dates need to be given"
                }
        if not extra_params:
            extra_params = {}
        url = f"{self.base_url}/cves/2.0/"
        query_params = {
            "cvssV3Severity": severity,
            "cweId": cwe_id,
            "keyword": keyword,
            "pubStartDate": published_start_date,
            "pubEndDate": published_end_date,
            "resultsPerPage": page_size,
            "startIndex": start_index
        }
        headers = {
            "apiKey": self.api_key
        }
        query_params.update(extra_params)
        response = BaseConnectorClass().request_handler(method=HttpMethods.GET.value, url=url,
                                                        query_params=query_params, headers=headers)
        return response

    def entrypoint(self, cve_id: str, extra_params: dict = None):
        """
        This action us used to get details of a particular CVE
        :param cve_id: Enter the CVE ID to get details of
        :param extra_params: Enter any extra params to add. Eg: addOns
        """
        url = f"{self.base_url}/cves/2.0/"
        query_params = {
            "cveId": cve_id
        }
        if extra_params:
            query_params.update(extra_params)
        headers = {
            "apiKey": self.api_key
        }
        response = BaseConnectorClass().request_handler(method=HttpMethods.GET.value, url=url,
                                                        headers=headers, query_params=query_params)
        return response
