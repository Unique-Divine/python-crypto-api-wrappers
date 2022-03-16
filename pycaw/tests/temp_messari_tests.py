"""Tests for 'pycaw.messari'."""
import os
import sys
import time
import pytest

from pycaw import messari 

import pandas as pd
from typing import Dict

API_KEY = os.getenv('MESSARI_API_KEY')
if API_KEY is None:
    print('Please define MESSARI_API_KEY in your runtime enviornment')
    sys.exit()

class TestMessari():
    """This is a unit testing class for testing the Messari class"""


    @pytest.fixture
    def messari_connector(self) -> messari.Messari:
        """Test initialization of the Messari class"""
        messari_connector = messari.Messari(API_KEY)
        assert isinstance(messari_connector, messari.Messari)
        return messari_connector

    def test_get_all_assets(self, messari_connector: messari.Messari):
        """Test get all assets"""
        response_data = messari_connector.get_all_assets()
        assert isinstance(response_data, Dict)

        response_data_df = messari_connector.get_all_assets(asset_fields=['metrics'], to_dataframe=True)
        assert isinstance(response_data_df, pd.DataFrame)

        metric = 'mining_stats'
        response_data_df_market_data = messari_connector.get_all_assets(asset_metric=metric,
                                                              to_dataframe=True)
        assert isinstance(response_data_df_market_data, pd.DataFrame)

        #dfs = [] # list to hold metric DataFrames
        #for i in range(1, 5, 1):
        #    df = messari.get_all_assets(page=1, limit=500,
        #                                asset_metric='marketcap', to_dataframe=True)
        #    dfs.append(df)
        #merged_df = pd.concat(dfs)
        #print(f'Number of assets in DataFrame {len(merged_df)}')
        #assert isinstance(merged_df, pd.DataFrame)
        #print('sleeping for 60 sec')
        #for i in range(20):
        #    print(f'sleep {i}/19')
        #    time.sleep(10)

    def test_get_asset(self, messari_connector: messari.Messari):
        """Test get asset"""

        assets = ['bitcoin', 'ethereum', 'tether']
        #asset_metadata = messari_connector.get_asset(asset_slugs=assets)
        #asset_metadata.head()

        fields = ['id', 'name']
        #asset_metadata_filtered = messari_connector.get_asset(asset_slugs=assets, asset_fields=fields)
        #asset_metadata_filtered.head()

    def test_get_asset_profile(self, messari_connector: messari.Messari):
        """Test get asset profile"""
        assets = ['bitcoin', 'ethereum', 'tether']
        asset_profile_data = messari_connector.get_asset_profile(asset_slugs=assets)
        assert isinstance(asset_profile_data, Dict)
        details = asset_profile_data['bitcoin']['profile_general_overview_project_details']
        assert isinstance(details, str)
        asset = 'Uniswap'
        profile_metric = 'investors'
        #governance_data = messari_connector.get_asset_profile(asset_slugs=asset,
        #                                            asset_profile_metric=profile_metric)
        #assert isinstance(governance_data, Dict)

    def test_get_asset_metric(self, messari_connector: messari.Messari):
        """Test get asset metirc"""
        assets = ['bitcoin', 'ethereum', 'tether']
        asset_metric_df = messari_connector.get_asset_metrics(asset_slugs=assets)
        assert isinstance(asset_metric_df, pd.DataFrame)
        #metric = 'marketcap'
        #asset_metric_df_marketcap = messari_connector.get_asset_metrics(asset_slugs=assets,
        #                                                      asset_metric=metric)
        #assert isinstance(asset_metric_df_marketcap, pd.DataFrame)

    def test_get_asset_market_data(self, messari_connector: messari.Messari):
        """Test get asset market date"""
        assets = ['bitcoin', 'ethereum', 'tether']
        market_data = messari.get_asset_market_data(asset_slugs=assets)
        assert isinstance(market_data, pd.DataFrame)

    def test_get_all_markets(self, messari_connector: messari.Messari):
        """Test get all markets"""
        markets_df = messari_connector.get_all_markets()
        assert isinstance(markets_df, pd.DataFrame)

    def test_get_metric_timeseries(self, messari_connector: messari.Messari):
        """Test get metic timeseries"""
        metric = 'price'
        start = '2020-06-01'
        end = '2021-01-01'
        assets = ['bitcoin', 'ethereum', 'tether']
        timeseries_df = messari_connector.get_metric_timeseries(asset_slugs=assets,
                                                      asset_metric=metric, start=start, end=end)
        assert isinstance(timeseries_df, pd.DataFrame)
