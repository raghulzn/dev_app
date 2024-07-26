import requests
from .constants import Constants, ErrorMessage, HttpMethods

"""
Connector Template Class
This class is aimed at being a template class which contains common methods used by connector/ SOAR engineers
Template Version: V1
Python version: 3.x
"""


class BaseConnectorClass(object):

    def __int__(self):
        self.template_version = "1.0.2"

    def request_handler(self, method: str, url: str,
                        query_params: dict = None,
                        payload_json: dict = None,
                        custom_output: str = None,
                        payload_data: object = None,
                        response_type: str = None,
                        download: bool = False,
                        filename: str = None,
                        timeout: int = None,
                        headers: dict = None,
                        auth: tuple = None,
                        verify: bool = True,
                        files: any = None,
                        **kwargs: object) -> dict:
        """
        This method is used to handle all requests in the class
        To use this method the 2 mandatory parameters are: 1) HTTP method to perform
                                                          2) URL to make the HTTP request to

        Authentication is supported via 5 methods in this request handler: 1) Basic authentication - Where the username and password are passed as arguments in the request handler
                                                                           2) Authentication over parameters - Where the authentication credentials can be passed over the query_params argument and are encoded into the request
                                                                           3) Authentication over headers - Where the authentication credentials can be passed over the headers argument and are sent along with the request
                                                                           4) Authentication over data - Where the authentication credentials can be passed over either the payload_json argument or payload_data argument. Difference being, payload_json sends data in the json part of the request while json_data sends data in the data part of the request
                                                                           5) Authentication over files - Where auth credentials can be passed over files

        We must note that this request handler currently is not capable of handling object/ 3rd party library based requests such as boto3 etc

        @param custom_output: Any custom response to return
        @param payload_json: Any data to pass in the JSON parameter of a request
        @param payload_data: Any data to pass in the data parameter of a request
        @param response_type: Response type received
        @param method: HTTP method to use
        @param url: url to make the request to
        @param query_params: Parameters to encode in the request URL
        @param download: Enter if any download is required
        @param filename: Enter the filename to save the downloaded data as
        @param timeout: Enter the timeout value
        @param headers: Enter any headers to pass in the request
        @param auth: Enter a tuple consisting of username and password to be passed in the request. Eg (username, password)
        @param verify: Should the certificate be verified or not. Defaults to True
        @param files: Files to pass w/ the request
        @return: A dictionary containing request response, and execution status of the request
        @rtype: dict
        """
        try:

            if not timeout:
                timeout = 15

            if method in [method_val.value for method_val in HttpMethods]:
                response = self.make_request(method=method,
                                             url=url,
                                             params=query_params,
                                             json_data=payload_json,
                                             payload_data=payload_data,
                                             headers=headers,
                                             timeout=timeout,
                                             auth=auth,
                                             verify=verify,
                                             files=files)

            else:

                return {Constants.ACTION_RESULT: ErrorMessage.INVALID_METHOD,
                        Constants.ACTION_STATUS: Constants.ERROR}

            if type(response) is not dict:
                response = self.process_request(response=response, download=download,
                                                filename=filename,
                                                custom_output=custom_output,
                                                response_type=response_type)
            return response

        except Exception as e:
            return {Constants.ACTION_RESULT: str(e),
                    Constants.ACTION_STATUS: Constants.ERROR}

    def make_request(self, method: str, url: str,
                     params: dict = None,
                     json_data: dict = None,
                     payload_data: any = None,
                     headers: dict = None,
                     timeout: int = None,
                     auth: tuple = None,
                     verify: bool = None,
                     files: any = None,
                     **kwargs):
        """
        This method is a supporting method for helping the request handler make a request using the requests module
        @param method: HTTP method to use
        @param url: url to make the request to
        @param params: Parameters to encode in the request URL
        @param timeout: Enter the timeout value
        @param headers: Enter any headers to pass in the request
        @param auth: Enter a tuple consisting of username and password to be passed in the request. Eg (username, password)
        @param payload_data: Any data to pass in the data parameter of a request
        @param verify: Should the certificate be verified or not. Defaults to True
        @param files: Files to pass w/ the request
        @param json_data: Any data to pass in the JSON parameter of a request
        """
        try:
            response = requests.request(method=method,
                                        url=url,
                                        params=params,
                                        json=json_data,
                                        data=payload_data,
                                        headers=headers,
                                        timeout=timeout,
                                        auth=auth,
                                        verify=verify,
                                        files=files)
            return response

        except Exception as e:
            return {Constants.ACTION_RESULT: str(e),
                    Constants.ACTION_STATUS: Constants.ERROR}

    def process_request(self, response: requests,
                        download: bool = None,
                        filename: any = None,
                        custom_output: str = None,
                        response_type: str = None,
                        **kwargs):
        """
        This method is a supporting method for helping the request handler process the request and format response into CSOL return format
        @param response: Pass the request class object to format
        @param download: Enter if any download is required
        @param filename: Enter the filename to save the downloaded data as
        @param custom_output: Any custom response to return
        @param response_type: Response type received
        """
        response_data = {Constants.STATUS_CODE: response.status_code}
        try:

            if response.ok:

                if download:

                    temp_folder = kwargs.get('temp_folder')
                    path = '{0}{1}'.format(temp_folder, filename)

                    with open(path, 'wb') as fd:

                        fd.write(response.content)
                        response_path = path

                    response_data[Constants.RESPONSE] = {'file_path': response_path}

                elif custom_output:
                    response_data[Constants.RESPONSE] = custom_output

                elif len(response.text) == 0:
                    response_data[Constants.RESPONSE] = ErrorMessage.NO_DATA_RETURNED

                elif response_type == Constants.RESPONSE_TYPE_TEXT:
                    response_data[Constants.RESPONSE] = response.text

                elif response_type == Constants.RESPONSE_TYPE_CONTENT:
                    response_data[Constants.RESPONSE] = response.content

                else:
                    response_data[Constants.RESPONSE] = response.json()

                execution_status = Constants.SUCCESS

            else:

                response_data[Constants.RESPONSE] = response.text
                execution_status = Constants.ERROR

        except Exception as e:
            response_data[Constants.RESPONSE] = str(e)
            execution_status = Constants.ERROR

        return {Constants.ACTION_RESULT: response_data,
                Constants.ACTION_STATUS: execution_status}

    def test_connection(self, response: requests,
                        custom_output: bool = False,
                        **kwargs):
        """
        Test Connection
        """
        try:
            if response.ok:
                execution_status = Constants.SUCCESS
                result = Constants.CREDENTIALS_VALID
                message = Constants.AUTH_SUCCESSFUL
                status_code = response.status_code
                if custom_output:
                    result = response.json()

            else:
                execution_status = Constants.ERROR
                result = Constants.AUTH_ERROR
                message = ErrorMessage.AUTH_FAILED
                status_code = response.status_code
                if custom_output:
                    result = response.text

        except Exception as e:
            execution_status = Constants.ERROR
            result = str(e)
            message = ErrorMessage.AUTH_FAILED
            status_code = response.status_code
            if custom_output:
                result = response.text

        return {
            Constants.ACTION_STATUS: execution_status,
            Constants.MESSAGE: message,
            Constants.ACTION_RESULT: result,
            Constants.STATUS_CODE: status_code
        }

