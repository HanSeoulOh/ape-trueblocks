import os
from typing import TYPE_CHECKING, Union

from ape.exceptions import ApeException
from requests import Response

from ape_trueblocks.utils import NETWORKS

if TYPE_CHECKING:
    from ape_trueblocks.types import SSHResponse, ResponseValue


class ApeTrueblocksException(ApeException):
    """
    A base exception in the ape-etherscan plugin.
    """


class SSHResponseError(ApeTrueblocksException):
    """
    Raised when the response is not correct.
    """

    def __init__(self, response: Union[Response, "SSHResponse"], message: str):
        if not isinstance(response, Response):
            response = response.response

        self.response = response
        super().__init__(f"Response indicated failure: {message}")


class UnhandledResultError(SSHResponseError):
    """
    Raised in specific client module where the result from Trueblocks
    has an unhandled form.
    """

    def __init__(self, response: Union[Response, "SSHResponse"], value: "ResponseValue"):
        message = f"Unhandled response format: {value}"
        super().__init__(response, message)



class ContractVerificationError(ApeTrueblocksException):
    """
    An error that occurs when unable to verify or publish a contract.
    """


def get_request_error(response: Response, ecosystem: str) -> SSHResponseError:
    response_data = response.json()
    if "result" in response_data and response_data["result"]:
        message = response_data["result"]
    elif "message" in response_data:
        message = response_data["message"]
    else:
        message = response.text

    # if "max rate limit reached" in response.text.lower():
    #     return EtherscanTooManyRequestsError(response, ecosystem)

    return SSHResponseError(response, message)