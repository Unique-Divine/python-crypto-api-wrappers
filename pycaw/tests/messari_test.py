"""Tests for 'pycaw.messari'."""
import os
import sys
import time
import pytest

from pycaw import messari

import pandas as pd
from typing import Dict, List

API_KEY = os.getenv("MESSARI_API_KEY")
if API_KEY is None:
    print("Please define MESSARI_API_KEY in your runtime enviornment")
    sys.exit()


class TestMessari:
    """This is a unit testing class for testing the Messari class"""

    @pytest.fixture
    def messari_connector(self) -> messari.Messari:
        """Test initialization of the Messari class"""
        messari_connector = messari.Messari(API_KEY)
        assert isinstance(messari_connector, messari.Messari)
        return messari_connector

    def test_get_all_assets(self, messari_connector: messari.Messari):
        """Test 'Messari.get_all_assets'."""

        response_data = messari_connector.get_all_assets()
        assert isinstance(response_data, Dict)

        response_data_df = messari_connector.get_all_assets(
            asset_fields=["metrics"], to_dataframe=True
        )
        assert isinstance(response_data_df, pd.DataFrame)

        metric = "mining_stats"
        response_data_df_market_data = messari_connector.get_all_assets(
            asset_metric=metric, to_dataframe=True
        )
        assert isinstance(response_data_df_market_data, pd.DataFrame)

    def test_get_asset(self, messari_connector: messari.Messari):
        """Test get asset"""

        assets: List[str] = ["bitcoin", "ethereum", "tether"]

        asset_metadata = messari_connector.get_asset(asset_slugs=assets)
        assert all(
            [col in asset_metadata.columns for col in ["name", "symbol", "slug", "id"]]
        )

        fields = ["id", "name"]
        asset_metadata_filtered = messari_connector.get_asset(
            asset_slugs=assets, asset_fields=fields
        )
        assert all([col in asset_metadata_filtered.columns for col in ["name", "id"]])

    def test_get_asset_profile(self, messari_connector: messari.Messari):
        """Test 'Messari.get_asset_profile'."""

        assets = ["bitcoin", "ethereum", "tether"]

        asset_profile_data = messari_connector.get_asset_profile(asset_slugs=assets)
        assert isinstance(asset_profile_data, Dict)
        details = asset_profile_data["bitcoin"][
            "profile_general_overview_project_details"
        ]
        assert isinstance(details, str)
        asset = "Uniswap"
        profile_metric = "investors"
        governance_data = messari_connector.get_asset_profile(
            asset_slugs=asset, asset_profile_metric=profile_metric
        )
        assert isinstance(governance_data, Dict)
        assert asset in governance_data
        expected_fields: List[str] = [
            "id",
            "slug",
            "profile_investors_individuals",
            "profile_investors_organizations",
        ]
        assert all([field in governance_data for field in expected_fields])

    def test_get_asset_metric(self, messari_connector: messari.Messari):
        """Test get asset metric"""
        assets = ["bitcoin", "ethereum", "tether"]
        asset_metric_df = messari_connector.get_asset_metrics(asset_slugs=assets)
        assert isinstance(asset_metric_df, pd.DataFrame)
        expected_fields: List[str] = ["id", "symbol", "market_data_price_usd"]
        assert all([col in asset_metric_df.columns for col in expected_fields])

    def test_get_asset_market_data(self, messari_connector: messari.Messari):
        """Test get asset market date"""
        assets = ["bitcoin", "ethereum", "tether"]
        market_data = messari_connector.get_asset_market_data(asset_slugs=assets)
        assert isinstance(market_data, pd.DataFrame)

    def test_get_all_markets(self, messari_connector: messari.Messari):
        """Test get all markets"""
        markets_df = messari_connector.get_all_markets()
        assert isinstance(markets_df, pd.DataFrame)

    def test_get_metric_timeseries(self, messari_connector: messari.Messari):
        """Test get metic timeseries"""
        metric = "price"
        start = "2020-06-01"
        end = "2021-01-01"
        assets = ["bitcoin", "ethereum", "tether"]
        timeseries_df = messari_connector.get_metric_timeseries(
            asset_slugs=assets, asset_metric=metric, start=start, end=end
        )
        assert isinstance(timeseries_df, pd.DataFrame)
