import pandas as pd
from pycaw import defillama as dl 


class TestDeFiLlama():
    """Test suite for the 'defillama.DeFiLlama' class."""

    def test_init(self):
        """Test initializing DeFiLlama class"""
        dl_conn = dl.DeFiLlama()
        assert isinstance(dl_conn, dl.DeFiLlama)

    def test_get_protocol_tvl(self):
        """Test getting protocol tvl"""
        dl_conn = dl.DeFiLlama()
        tvl = dl_conn.get_protocol_tvl_timeseries(
            ["aave", "compound"], start_date="2021-10-01", end_date="2021-10-10"
        )
        assert isinstance(tvl, pd.DataFrame)

    def test_global_tvl(self):
        """Test getting global tvl"""
        dl_conn = dl.DeFiLlama()
        global_tvl = dl_conn.get_global_tvl_timeseries(
            start_date="2021-10-01", end_date="2021-10-10"
        )
        assert isinstance(global_tvl, pd.DataFrame)

    def test_chain_tvl(self):
        """Test getting chain tvl"""
        dl_conn = dl.DeFiLlama()
        chains = ["Avalanche", "Harmony", "Polygon"]
        chain_tvl = dl_conn.get_chain_tvl_timeseries(
            chains, start_date="2021-10-01", end_date="2021-10-10"
        )
        assert isinstance(chain_tvl, pd.DataFrame)

    def test_current_tvl(self):
        """Test getting current protocol tvl"""
        dl_conn = dl.DeFiLlama()
        protocols = ["uniswap", "curve", "aave"]
        current_tvl = dl_conn.get_current_tvl(protocols)
        assert isinstance(current_tvl, pd.DataFrame)

    def test_get_protocols(self):
        """Test getting protocol info"""
        dl_conn = dl.DeFiLlama()
        protocols = dl_conn.get_protocols()
        assert isinstance(protocols, pd.DataFrame)