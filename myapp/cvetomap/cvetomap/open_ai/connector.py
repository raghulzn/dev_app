# !/usr/bin/env python

import requests
import json
from .constants import Constants, HttpMethods, ErrorMessage
from .base_connector_class import BaseConnectorClass

"""
OpenAI Connector
Connector Description: OpenAI is an AI research and deployment company. OpenAI provides various artificial intelligence models such as GPT-3, Codex etc. that enables natural interfaces with large scale models.
Connector Category: IT Services
Authentication supported: API Key
Connector Version: 1.0.0
Supported Version: 1.0.0
Documentation URL: 
Release Notes: This is the initial release of the OpenAI connector with actions related to working alongside large scale NLP models
"""


class OpenAiConnector(object):
    def __init__(self, api_token: str,
                 **kwargs):
        """
        This is used to initialise values across the connector
        :param api_token: Enter the API token to authenticate to OpenAI with
        """

        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": "Bearer {0}".format(api_token),
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def test_connection(self) -> dict:
        """
        Test Connectivity of endpoint w/ provided creds
        """
        url = f"{self.base_url}/models"
        response = BaseConnectorClass().request_handler(method=HttpMethods.GET.value, url=url, headers=self.headers)
        return response

    def action_get_all_models(self, **kwargs) -> dict:
        """
        This action is used to get a list of all models the user has access to
        """
        url = f"{self.base_url}/models"
        response = BaseConnectorClass().request_handler(method=HttpMethods.GET.value,
                                                        url=url,
                                                        headers=self.headers)
        return response

    def action_get_model_details(self, model_identifier: str):
        """
        This action is used to get details of a model in OpenAI
        :param model_identifier: Enter the identifier of the model to get details of. Eg: text-davinci-003
        """
        url = f"{self.base_url}/models/{model_identifier}"
        response = BaseConnectorClass().request_handler(method=HttpMethods.GET.value,
                                                        url=url,
                                                        headers=self.headers)
        return response

    def action_create_completion(
            self,
            model_identifier: str,
            prompt: str,
            max_tokens: int = 256,
            temperature: float = 0.7,
            top_p: float = 1,
            frequency_penalty: float = 0,
            presence_penalty: float = 0,
            stop: str = None,
            n: int = 1,
            **kwargs) -> dict:
        """
            This action is used to get a completion from a model
            :param model_identifier: Enter the identifier of the model to get completion from. Eg: text-davinci-003
            :param prompt: Enter the prompt to get completion from
            :param max_tokens: Enter the maximum number of tokens to return. Defaults to 256
            :param temperature: Enter the temperature to use for sampling. Defaults to 0.7
            :param top_p: Enter the top_p to use for sampling. Defaults to 1
            :param frequency_penalty: Enter the frequency penalty to use for sampling. Defaults to 0
            :param presence_penalty: Enter the presence penalty to use for sampling. Defaults to 0
            :param stop: Enter the stop sequence to use for sampling. Defaults to \n
            :param n: Enter the number of samples to return. Defaults to 1
            """
        url = f"{self.base_url}/completions"
        payload = {
            "model": model_identifier,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "n": n
        }
        if stop:
            payload["stop"] = stop
        response = BaseConnectorClass().request_handler(method=HttpMethods.POST.value,
                                                        url=url,
                                                        headers=self.headers,
                                                        payload_json=payload,
                                                        timeout=100
                                                        )
        return response

    def action_edit_prompt(
            self,
            model: str,
            input: str,
            instruction: str,
            n: int = 1,
            temperature: int = 1,
            top_p: int = 1,
            **kwargs
    ) -> dict:
        """
        This action is used to edit a prompt
        :param model: Enter the identifier of the model to get completion from. Eg: text-davinci-003
        :param input: Enter the prompt to get completion from
        :param instruction: Enter the instruction to use for sampling. Defaults to \n
        :param n: Enter the number of samples to return. Defaults to 1
        :param temperature: Enter the temperature to use for sampling. Defaults to 1
        :param top_p: Enter the top_p to use for sampling. Defaults to 1
        """
        url = f"{self.base_url}/edits"
        payload = {
            "model": model,
            "input": input,
            "instruction": instruction,
            "n": n,
            "temperature": temperature,
            "top_p": top_p
        }
        response = BaseConnectorClass().request_handler(method=HttpMethods.POST.value,
                                                        url=url,
                                                        headers=self.headers,
                                                        payload_json=payload)
        return response

    def action_create_image(
            self,
            prompt: str,
            n: int = 1,
            size: str = "1024x1024",
            **kwargs
    ) -> dict:
        """
        This action is used to create an image
        :param prompt: Enter the prompt to get image completion from
        :param n: Enter the number of samples to return. Defaults to 1
        :param size: Enter the size of the image to return. Defaults to 1024x1024
        """
        url = f"{self.base_url}/images/generations"
        payload = {
            "prompt": prompt,
            "n": n,
            "size": size
        }
        response = BaseConnectorClass().request_handler(method=HttpMethods.POST.value,
                                                        url=url,
                                                        headers=self.headers,
                                                        payload_json=payload)
        return response

    def entrypoint(self, model: str, messages: list, extra_params: dict = None, **kwargs):
        """
        This action is used to create a chat completion
        :param model: Enter the identifier of the model to get completion from. Eg: text-davinci-003
        :param messages: Enter a list of messages to use for sampling. This should be compliant with this - https://platform.openai.com/docs/api-reference/chat/create
        :param extra_params: Enter extra parameters to use for sampling. Defaults to None
        """
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": messages,
            "response_format": {
                "type": "json_object"
            }
        }
        if extra_params:
            payload.update(extra_params)
        response = BaseConnectorClass().request_handler(method=HttpMethods.POST.value,
                                                        timeout=600, url=url, headers=self.headers,
                                                        payload_json=payload)
        return response

    def action_generic_action(self, endpoint: str, method: str, query_params: dict = None, payload: dict = None, **kwargs) -> dict:
        """
        This action is used to perform a generic action
        :param endpoint: Enter the url to perform the action on
        :param method: Enter the method to use for the action
        :param query_params: Enter extra parameters to use for the action.
        :param payload: Enter the payload to use for the action
        """
        url = f"{self.base_url}/{endpoint}"
        response = BaseConnectorClass().request_handler(method=method.upper(),
                                                        url=url,
                                                        query_params=query_params,
                                                        headers=self.headers,
                                                        payload_json=payload)
        return response

