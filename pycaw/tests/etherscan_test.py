#!/usr/bin/env python
# import __init__

import os
import json
import pytest

from pycaw import eth
from pycaw import etherscan
from pycaw.etherscan.token_info_connector import TokenInfoMap, TokenID

from typing import Any, Dict, List, Optional, Union


class TestEtherscanConnector:
    @pytest.fixture
    def connector(self) -> etherscan.EtherscanConnector:
        return etherscan.EtherscanConnector()

    def test_get_tx_receipt(self, connector: etherscan.EtherscanConnector):
        tx_hash: str = (
            "0x20f98d428f3452a858ddb0972628991f50c529fbc5883111d1db1e6ba2eb4121"
        )
        tx_receipt: Dict[str, Any] = connector.get_tx_receipt(tx_hash=tx_hash)
        assert tx_receipt

        if isinstance(tx_receipt, dict):
            assert all([isinstance(key, str) for key in tx_receipt])
        elif isinstance(tx_receipt, str):
            assert "please use API Key" in tx_receipt
        else:
            assert False

    def test_get_tx_gas_info(self, connector: etherscan.EtherscanConnector):
        tx_hash: str = (
            "0xe61b59cbe8381dff1c3152545f63c7bbdf03f27411a183c12bd7f90b68daf27a"
        )
        gas_info: eth.GasInfo = connector.get_tx_gas_info(tx_hash=tx_hash)
        assert isinstance(gas_info, eth.GasInfo)
        assert gas_info.gas_price_wei > 0
        if gas_info.eth_price_usd:
            assert gas_info.eth_price_usd > 0
        else:
            assert gas_info.eth_price_usd is None
        assert gas_info.tx_hash


class TestTokenInfoConnector:
    @pytest.fixture
    def connector(self) -> etherscan.TokenInfoConnector:
        return etherscan.TokenInfoConnector()

    def test_single_query(self, connector: etherscan.TokenInfoConnector):
        token_id = "0x0e3a2a1f2146d86a604adc220b4967a898d7fe07"
        token_info_map: TokenInfoMap = connector.get_token_info(token_ids=token_id)
        assert isinstance(token_info_map, dict)
        assert all([isinstance(token_id, TokenID) for token_id in token_info_map])

    @pytest.fixture
    def token_info_map(self, connector: etherscan.TokenInfoConnector) -> TokenInfoMap:
        token_id_wbtc: str = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"
        token_id_card: str = "0x0e3a2a1f2146d86a604adc220b4967a898d7fe07"
        token_ids: List[str] = [token_id_wbtc, token_id_card]

        token_info_map: TokenInfoMap = connector.get_token_info(token_ids=token_ids)
        assert isinstance(token_info_map, dict)
        assert all([isinstance(token_id, TokenID) for token_id in token_info_map])
        return token_info_map

    def test_save_token_info_json(
        self,
        connector: etherscan.TokenInfoConnector,
        token_info_map: TokenInfoMap,
        save_dir: Optional[str] = None,
    ):
        """l."""
        save_dir: str = "_test_temp"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        connector.save_token_info_json(token_info_map=token_info_map, save_dir=save_dir)

        save_path: str = os.path.join(save_dir, "token_info.json")
        with open(save_path, mode="r") as f:
            map_from_file: TokenInfoMap = json.load(f)

        for token_id in token_info_map:
            assert token_id in map_from_file, f"Failed to save token id: {token_id}"

        os.remove(path=save_path)
