
from .connector import NvdConnector
import requests_mock
from .constants import Constants, HttpMethods
from unittest import TestCase
import pytest


class TestNvdConnector(TestCase):
    def _set_up_mock(self, mock_):
        mock_.get(requests_mock.ANY, json={"dummy": "dummy"})
        mock_.delete(requests_mock.ANY, json={"dummy": "dummy"})
        mock_.post(requests_mock.ANY, json={"dummy": "dummy"})
        mock_.patch(requests_mock.ANY, json={"dummy": "dummy"})
        mock_.put(requests_mock.ANY, json={"dummy": "dummy"})

    def setUp(self):
        self.test_connector = NvdConnector(api_key='dummy')

    @requests_mock.Mocker()
    def test_test_connection(self, mocker):
        self._set_up_mock(mocker)
        response = self.test_connector.test_connection()
        self.assertEqual(Constants.SUCCESS, response.get(Constants.ACTION_STATUS))

    @requests_mock.Mocker()
    def test_action_list_cves(self, mocker):
        self._set_up_mock(mocker)
        response = self.test_connector.action_list_cves(severity='dummy', cwe_id='dummy', keyword='dummy', published_start_date='dummy', published_end_date='dummy', page_size=1, start_index=1, extra_params={'dummy': 'dummy'})
        self.assertEqual(Constants.SUCCESS, response.get(Constants.ACTION_STATUS))

    @requests_mock.Mocker()
    def test_action_get_cve_details(self, mocker):
        self._set_up_mock(mocker)
        response = self.test_connector.action_get_cve_details(cve_id='dummy', extra_params={'dummy': 'dummy'})
        self.assertEqual(Constants.SUCCESS, response.get(Constants.ACTION_STATUS))
