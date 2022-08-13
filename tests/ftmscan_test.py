from pycaw import ftmscan
from typing import List
import pytest


class TestFTMScanConnector:
    @pytest.fixture
    def ftmscan_api(self) -> ftmscan.FTMScanConnector:
        return ftmscan.FTMScanConnector()

    def test_connector(self, ftmscan_api: ftmscan.FTMScanConnector):
        address = "0x33e0e07ca86c869ade3fc9de9126f6c73dad105e"
        balance: float = ftmscan_api.account_balance_single_address(address=address)
        assert isinstance(balance, float)
        assert balance >= 0

    def test_tx_list(self, ftmscan_api: ftmscan.FTMScanConnector):
        address = "0xba821dc848803900C01BA7Ac1D7a034B95B1eD97"
        tx_receipts: List[ftmscan.TxReceipt] = ftmscan_api.tx_receipt_list(
            address=address
        )
        assert isinstance(tx_receipts, (list))

        if not len(tx_receipts) > 0:
            return

        tx_receipt = tx_receipts[0]
        assert isinstance(tx_receipt, dict)
        assert "gasPrice" in tx_receipt.keys()
