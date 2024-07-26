from .connector import OpenAiConnector
import requests_mock
from .constants import Constants, HttpMethods
from unittest import TestCase
import pytest


class TestOpenAiConnector(TestCase):
    def _set_up_mock(self, mock_):
        mock_.get(requests_mock.ANY, json={"dummy": "dummy"})
        mock_.delete(requests_mock.ANY, json={"dummy": "dummy"})
        mock_.post(requests_mock.ANY, json={"dummy": "dummy"})
        mock_.patch(requests_mock.ANY, json={"dummy": "dummy"})
        mock_.put(requests_mock.ANY, json={"dummy": "dummy"})

    def setUp(self):
        self.test_connector = OpenAiConnector(api_token='dummy')

    @requests_mock.Mocker()
    def test_test_connection(self, mocker):
        self._set_up_mock(mocker)
        response = self.test_connector.test_connection()
        self.assertEqual(Constants.SUCCESS, response.get(Constants.ACTION_STATUS))

    @requests_mock.Mocker()
    def test_action_get_all_models(self, mocker):
        self._set_up_mock(mocker)
        response = self.test_connector.action_get_all_models()
        self.assertEqual(Constants.SUCCESS, response.get(Constants.ACTION_STATUS))

    @requests_mock.Mocker()
    def test_action_get_model_details(self, mocker):
        self._set_up_mock(mocker)
        response = self.test_connector.action_get_model_details(model_identifier='dummy')
        self.assertEqual(Constants.SUCCESS, response.get(Constants.ACTION_STATUS))

    @requests_mock.Mocker()
    def test_action_create_completion(self, mocker):
        self._set_up_mock(mocker)
        response = self.test_connector.action_create_completion(model_identifier='dummy', prompt='dummy', max_tokens=1,
                                                                temperature=['dummy'], top_p=['dummy'],
                                                                frequency_penalty=['dummy'], presence_penalty=['dummy'],
                                                                stop='dummy', n=1)
        self.assertEqual(Constants.SUCCESS, response.get(Constants.ACTION_STATUS))

    @requests_mock.Mocker()
    def test_action_edit_prompt(self, mocker):
        self._set_up_mock(mocker)
        response = self.test_connector.action_edit_prompt(model='dummy', input='dummy', instruction='dummy', n=1,
                                                          temperature=1, top_p=1)
        self.assertEqual(Constants.SUCCESS, response.get(Constants.ACTION_STATUS))

    @requests_mock.Mocker()
    def test_action_create_image(self, mocker):
        self._set_up_mock(mocker)
        response = self.test_connector.action_create_image(prompt='dummy', n=1, size='dummy')
        self.assertEqual(Constants.SUCCESS, response.get(Constants.ACTION_STATUS))

    @requests_mock.Mocker()
    def test_action_create_chat_completion(self, mocker):
        self._set_up_mock(mocker)
        response = self.test_connector.action_create_chat_completion(model='dummy', messages=['dummy'], extra_params={'dummy': 'dummy'})
        self.assertEqual(Constants.SUCCESS, response.get(Constants.ACTION_STATUS))

    @requests_mock.Mocker()
    def test_action_generic_action(self, mocker):
        self._set_up_mock(mocker)
        response = self.test_connector.action_generic_action(endpoint='dummy', method='GET', query_params={'dummy': 'dummy'}, payload={'dummy': 'dummy'})
        self.assertEqual(Constants.SUCCESS, response.get(Constants.ACTION_STATUS))
