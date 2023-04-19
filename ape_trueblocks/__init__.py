# Add module top-level imports here
from ape import plugins

# from .explorer import Etherscan
from .query import TrueblocksQueryEngine


@plugins.register(plugins.QueryPlugin)
def query_engines():
    yield TrueblocksQueryEngine