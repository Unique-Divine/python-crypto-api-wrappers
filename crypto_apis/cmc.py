"""Coin Market Cap API wrapper.

Classes:
    CoinMarketCapAPI
    CoinMarketCapEndpoint
"""
import requests
from requests import exceptions
import ratelimit
import time
import os
import json
import tenacity
import logging
from typing import Any, Dict, List, Optional, Sequence, Union

from crypto_apis import secret_api_keys

# https://pro-api.coinmarketcap.com/v1/cryptocurrency/map

class CoinMarketCapAPI:
    """Python connector the Coin Market Cap API.

    Attributes:
        API_KEY (str)
    """

    endpoint_preamble = "" # TODO
    API_KEY: str = secret_api_keys.COINMARKETCAP_API_KEY 

    # @ratelimit.limits(calls=2, period=1) 
    def run_query(self, 
                  endpoint: str, 
                  params: Dict[str, str]) -> Union[list, dict]:
        """Note, Etherscan restricts the token_info query to 2 calls per second.
        
        Args: 
            endpoint (str): URL/API endpoint to query with `Requests.request.get()`
            params (Dict[str, str]): TODO
        
        Returns: 
            (dict): Component of the Requests.Response object
        """

        headers = {
            "Accepts": "application/json", 
            "Accept-Encoding": "deflate, gzip",
            "X-CMC_PRO_API_KEY": self.API_KEY}

        session = requests.Session()
        session.headers.update(headers)

        try:
            response: requests.Response = session.get(
                endpoint, headers=headers, params=params)
            if response and response.ok:
                return response.json()
            else:
                msg = (f"Failed request with status code {response.status_code}"
                       + f": {response.text}")
                logging.warning(msg)
                raise Exception(msg)
        except (exceptions.ConnectionError, 
                exceptions.Timeout, 
                exceptions.TooManyRedirects) as e:
            logging.exception("\n".join([
                f"ConnectionError: {e[0]}", f"Timeout: {e[1]}", 
                f"TooManyRedirects: {e[2]}"]))
            raise # Raise so retry can retry
        except Exception as e:
            logging.exception(f"Exception raised: {e}")
            raise # Raise so retry can retry
    
    def cmc_id_map(self, 
                   symbols: Union[str, Sequence[str]], 
                   save: bool = False) -> List[dict]:
        """
        Docs: https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyMap 
        """
        endpoint: str = CoinMarketCapEndpoint(
            category="cryptocurrency", path="map")
        if isinstance(symbols, str):
            symbols = [symbols]
        assert isinstance(symbols, list)

        # Query expects a comma-separated list of cryptocurrency symbols.
        excluded_symbols = ['EWTB']

        if symbols != ["all"]:    
            symbols: str = ",".join(symbols)
            symbols = symbols.replace("EWTB", "EWT")
            params: Dict[str, str] = dict(symbol=symbols)
        else:
            params = {}

        cmc_id_maps: List[dict] = self.run_query(
            endpoint=endpoint, params=params)["data"]

        if save: 
            self._save_cmc_id_maps(cmc_id_maps=cmc_id_maps)

        return cmc_id_maps
    
    def _save_cmc_id_maps(self, 
                          cmc_id_maps: List[dict], 
                          filename: Optional[str] = None, 
                          save_dir: Optional[str] = None) -> None:
        cmc_id_maps: List[dict] = sorted(
            cmc_id_maps, key=lambda dict_: dict_["id"])

        if filename is None:
            filename = "cmc_id_maps.json"
        if filename[-5:] != ".json":
            raise ValueError(f"Filename: {filename} must end in '.json'.")
        
        if save_dir:
            if not os.path.exists(save_dir):
                raise ValueError("")
            save_path: str = os.path.join(save_dir, filename)
        else:
            save_path = filename

        if os.path.exists(save_path):
            with open(file=save_path, mode="r") as f:
                current_cmc_id_maps = json.load(f)
                if current_cmc_id_maps is None:
                    current_cmc_id_maps = {}
            for map_ in current_cmc_id_maps:
                if map_ not in cmc_id_maps:
                    cmc_id_maps.append(map_)
        cmc_id_maps_json: List[dict] = cmc_id_maps
        
        with open(save_path, "w") as f:
            json.dump(cmc_id_maps_json, f, indent=3)


class CoinMarketCapEndpoint(str): 
    """
    Args & Attributes: 
        category (str): CMC endpoint category.
        path (str): CMC endpoint path.
    
    Endpoint categories:
        cryptocurrency: Endpoints that return data around cryptocurrencies such 
            as ordered cryptocurrency lists or price and volume data.
        exchange: Endpoints that return data around cryptocurrency exchanges 
            such as ordered exchange lists and market pair data.
        global-metrics: Endpoints that return aggregate market data such as 
            global market cap and BTC dominance.
        tools: Utilities such as cryptocurrency and fiat price conversions.
        blockchain: Endpoints that return block explorer related data.
        fiat: Endpoints that return data around fiats currencies including 
            mapping to CMC IDs.
        partners: Endpoints for convenient access to 3rd party crypto data.
        key: API key administration endpoints to review and manage your usage.

    Endpoint paths:
        latest: Latest market data. Latest market ticker quotes and averages for 
            cryptocurrencies and exchanges.
        historical: Historical market data. Intervals of historic market data 
            like OHLCV data or data for use in charting libraries.
        info: Metadata. Cryptocurrency and exchange metadata like block explorer
            URLs and logos.
        map: ID maps. Utility endpoints to get a map of resources to 
            CoinMarketCap IDs.
    """

    endpoint_categories: List[str] = [
        "cryptocurrency", "exchange", "global-metrics", "tools", "blockchain", 
        "fiat", "partners", "key"]
    endpoint_paths: List[str] = ["latest", "historical", "info", "map"]
    preamble_v1: str = "https://pro-api.coinmarketcap.com/v1"

    def __new__(cls, category: str, path: str) -> str:
        if category not in cls.endpoint_categories:
            raise ValueError("") # TODO
        if path not in cls.endpoint_paths:
            raise ValueError("") # TODO

        url_components = [cls.preamble_v1, category, path]
        url = "/".join(url_components)
        return url
    
    
        