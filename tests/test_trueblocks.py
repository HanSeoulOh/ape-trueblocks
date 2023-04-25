from typing import Callable

import pytest
from ape import accounts
from ape import logging

import ape

from ape_trueblocks.utils import NETWORKS
from ape_trueblocks.exceptions import ApeTrueblocksException
from ape_trueblocks.client import RemoteClient
# A map of each mock response to its contract name for testing `get_contract_type()`.
EXPECTED_CONTRACT_NAME_MAP = {
    "get_contract_response": "BoredApeYachtClub",
    "get_proxy_contract_response": "MIM-UST-f",
    "get_vyper_contract_response": "yvDAI",
}
TRANSACTION = "0x0da22730986e96aaaf5cedd5082fea9fd82269e41b0ee020d966aa9de491d2e6"
PUBLISH_GUID = "123"

# Every supported ecosystem / network combo as `[("ecosystem", "network") ... ]`
ecosystems_and_networks = [
    p
    for plist in [
        [(e, n) for n in nets] + [(e, f"{n}-fork") for n in nets] for e, nets in NETWORKS.items()
    ]
    for p in plist
]

base_url_test = pytest.mark.parametrize(
    "ecosystem,network,url",
    [
        ("ethereum", "mainnet", "etherscan.io"),
        ("ethereum", "mainnet-fork", "etherscan.io"),
        ("ethereum", "goerli", "goerli.etherscan.io"),
        ("ethereum", "goerli-fork", "goerli.etherscan.io"),
        ("ethereum", "sepolia", "sepolia.etherscan.io"),
        ("fantom", "opera", "ftmscan.com"),
        ("fantom", "opera-fork", "ftmscan.com"),
        ("fantom", "testnet", "testnet.ftmscan.com"),
        ("fantom", "testnet-fork", "testnet.ftmscan.com"),
        ("arbitrum", "mainnet", "arbiscan.io"),
        ("arbitrum", "mainnet-fork", "arbiscan.io"),
        ("arbitrum", "goerli", "goerli.arbiscan.io"),
        ("arbitrum", "goerli-fork", "goerli.arbiscan.io"),
        ("optimism", "mainnet", "optimistic.etherscan.io"),
        ("optimism", "mainnet-fork", "optimistic.etherscan.io"),
        ("optimism", "goerli", "goerli-optimism.etherscan.io"),
        ("optimism", "goerli-fork", "goerli-optimism.etherscan.io"),
        ("polygon", "mainnet", "polygonscan.com"),
        ("polygon", "mainnet-fork", "polygonscan.com"),
        ("polygon", "mumbai", "mumbai.polygonscan.com"),
        ("polygon", "mumbai-fork", "mumbai.polygonscan.com"),
        ("avalanche", "mainnet", "snowtrace.io"),
        ("avalanche", "fuji", "testnet.snowtrace.io"),
        ("bsc", "mainnet", "bscscan.com"),
        ("bsc", "mainnet-fork", "bscscan.com"),
        ("bsc", "testnet", "testnet.bscscan.com"),
        ("bsc", "testnet-fork", "testnet.bscscan.com"),
    ],
)

@base_url_test
def test_get_address_url(ecosystem, network, url, address, get_explorer):
    expected = f"https://{url}/address/{address}"
    explorer = get_explorer(ecosystem, network)
    actual = explorer.get_address_url(address)
    assert actual == expected


def test_ssh_connection():
