"""TODO module docs for crypto_apis.etherscan"""
from crypto_apis.etherscan import types 
from crypto_apis.etherscan import etherscan_connector
from crypto_apis.etherscan import token_info_connector 

EtherscanConnector = etherscan_connector.EtherscanConnector 
TokenInfoConnector = token_info_connector.TokenInfoConnector
# TokenInfoConnector.__doc__ = 
"""TODO doc"""

InternalMsgCall = types.InternalMsgCall
NormalTx = types.NormalTx
TxReceipt = types.TxReceipt

__all__ = ['EtherscanConnector', 'TokenInfoConnector']
