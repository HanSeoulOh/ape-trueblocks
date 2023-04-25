import json
import os
import random
import subprocess
from io import StringIO
from typing import Dict, Iterator, List, Optional

# from ape.logging import logger
# import ape.logging import logger

from ape_trueblocks.types import SourceCodeResponse
from ape_trueblocks.exceptions import UnhandledResultError

class _SSHClient:
    DEFAULT_CMD_PREFIX = "source $HOME/.zshrc; "

    def __init__(self, host: str, user: str, key_path: str, port: int = 22):
        self._host = host
        self._port = port
        self._user = user
        self._key_path = key_path

    def _ssh(self, cmd: str) -> str:
        ssh_cmd = f"ssh -i {self._key_path} -p {self._port} {self._user}@{self._host} {self.DEFAULT_CMD_PREFIX}{cmd}"
        # logger.debug(f"Sending command: {ssh_cmd} to TrueBlocks node at {self._host}")
        return subprocess.check_output(ssh_cmd, shell=True).decode("utf-8")

class RemoteClient(_SSHClient):
    def __init__(self, host: str, user: str, key_path: str, port: int = 22):
        super().__init__(host, user, key_path, port)

    def get_help(self) -> SourceCodeResponse:
        cmd = f"chifra -list"
        result = self._ssh(cmd)

        if not result:
            return SourceCodeResponse(name = 'ERROR')

        return SourceCodeResponse(name=result)
    
# class ContractClient(_SSHClient):
#     def __init__(self, ecosystem_name: str, network_name: str, address: str):
#         self._address = address
#         super().__init__(ecosystem_name, network_name, "contract")

#     def get_source_code(self) -> SourceCodeResponse:
#         params = {
#             **self.base_params,
#             "action": "getsourcecode",
#             "address": self._address,
#         }
#         result = self._get(params=params)
#         result_list = result.value or []

#         if not result_list:
#             return SourceCodeResponse()

#         elif len(result_list) > 1:
#             raise UnhandledResultError(result, result_list)

#         data = result_list[0]
#         if not isinstance(data, dict):
#             raise UnhandledResultError(result, data)

#         abi = data.get("ABI") or ""
#         name = data.get("ContractName") or "unknown"
#         return SourceCodeResponse(abi, name)

#     def verify_source_code(
#         self,
#         standard_json_output: Dict,
#         compiler_version: str,
#         contract_name: Optional[str] = None,
#         optimization_used: bool = False,
#         optimization_runs: Optional[int] = 200,
#         constructor_arguments: Optional[str] = None,
#         evm_version: Optional[str] = None,
#         license_type: Optional[int] = None,
#         libraries: Optional[Dict[str, str]] = None,
#     ) -> str:
#         libraries = libraries or {}
#         if len(libraries) > 10:
#             raise ValueError(f"Can only have up to 10 libraries (received {len(libraries)}).")

#         if not compiler_version.startswith("v"):
#             compiler_version = f"v{compiler_version}"

#         json_dict = {
#             **self.base_params,
#             "action": "verifysourcecode",
#             "codeformat": "solidity-standard-json-input",
#             "compilerversion": compiler_version,
#             "constructorArguements": constructor_arguments,
#             "contractaddress": self._address,
#             "contractname": contract_name,
#             "evmversion": evm_version,
#             "licenseType": license_type,
#             "optimizationUsed": int(optimization_used),
#             "runs": optimization_runs,
#             "sourceCode": StringIO(json.dumps(standard_json_output)),
#         }

#         iterator = 1
#         for lib_address, lib_name in libraries.items():
#             json_dict[f"libraryname{iterator}"] = lib_name
#             json_dict[f"libraryaddress{iterator}"] = lib_address
#             iterator += 1

#         headers = {"Content-Type": "application/x-www-form-urlencoded"}
#         return str(self._post(json_dict=json_dict, headers=headers).value)

#     def check_verify_status(self, guid: str) -> str:
#         json_dict = {**self.base_params, "action": "checkverifystatus", "guid": guid}
#         response = self._get(params=json_dict, raise_on_exceptions=False)
#         return str(response.value)


# class AccountClient(_SSHClient):
#     def __init__(self, ecosystem_name: str, network_name: str, address: str):
#         self._address = address
#         super().__init__(ecosystem_name, network_name, "account")

#     def get_all_normal_transactions(
#         self,
#         start_block: Optional[int] = None,
#         end_block: Optional[int] = None,
#         offset: int = 100,
#         sort: str = "asc",
#     ) -> Iterator[Dict]:
#         page_num = 1
#         last_page_results = offset  # Start at offset to trigger iteration
#         while last_page_results == offset:
#             page = self._get_page_of_normal_transactions(
#                 page_num, start_block, end_block, offset=offset, sort=sort
#             )

#             if len(page):
#                 yield from page

#             last_page_results = len(page)
#             page_num += 1

#     def _get_page_of_normal_transactions(
#         self,
#         page: int,
#         start_block: Optional[int] = None,
#         end_block: Optional[int] = None,
#         offset: int = 100,
#         sort: str = "asc",
#     ) -> List[Dict]:
#         params = {
#             **self.base_params,
#             "action": "txlist",
#             "address": self._address,
#             "startblock": start_block,
#             "endblock": end_block,
#             "page": page,
#             "offset": offset,
#             "sort": sort,
#         }
#         result = self._get(params=params)

#         if not isinstance(result.value, list):
#             raise UnhandledResultError(result, result.value)

#         return result.value


# class ClientFactory:
#     def __init__(self, ecosystem_name: str, network_name: str):
#         self._ecosystem_name = ecosystem_name
#         self._network_name = network_name

#     def get_contract_client(self, contract_address: str) -> ContractClient:
#         return ContractClient(self._ecosystem_name, self._network_name, contract_address)

#     def get_account_client(self, account_address: str) -> AccountClient:
#         return AccountClient(self._ecosystem_name, self._network_name, account_address)