import json
from dataclasses import dataclass
from typing import Dict, List, Union

from ape.utils import cached_property
from ape_trueblocks.exceptions import SSHResponseError

@dataclass
class SourceCodeResponse:
    abi: str = ""
    name: str = "unknown"


ResponseValue = str


class SSHResponse:
    retvalue: str =""