#!/usr/bin/env python
# import __init__

from pycaw import eth

from typing import Any, Dict, List, Optional, Union


class TestGasInfo:
    def test_init(self):
        tx_hash: str = (
            "0xe61b59cbe8381dff1c3152545f63c7bbdf03f27411a183c12bd7f90b68daf27a"
        )
        raw_tx_receipt: dict = {"cumulativeGasUsed": "0xd7e11b", "gasUsed": "0x2043b"}
        gas_info = eth.GasInfo(
            gas_used_wei=int(raw_tx_receipt["gasUsed"], base=16),
            gas_price_wei=int(raw_tx_receipt["cumulativeGasUsed"], base=16),
            tx_hash=tx_hash,
        )
        assert gas_info
        assert gas_info.eth_price_usd is None
        assert gas_info.timestamp is None
