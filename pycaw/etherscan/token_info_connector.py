from typing import Any, Dict, List, Optional, Union
import requests
import ratelimit
import time
import os
import json
import tenacity
import logging
from pycaw.etherscan import etherscan_connector

TokenID = str
TokenInfo = Dict[str, str]
TokenInfoMap = Dict[TokenID, TokenInfo]

class TokenInfoConnector(etherscan_connector.EtherscanConnector):
    """An Etherscan API connector for gathering token info. 
    
    Note, Etherscan restricts the token_info query to 2 calls per second.

    Attributes:
        API_KEY (str)

    Methods: 
        run_query
        get_token_info
        save_token_info_json
    """

    endpoint_preamble = "https://api.etherscan.io/api?"
    API_KEY: str

    def __init__(self, max_api_calls_sec: int = 2):
        self._api_call_sleep_time = 1 / max_api_calls_sec

    def _token_info_query_url(self, token_id: str) -> str:
        return "".join([
            self.endpoint_preamble, "module=token", "&action=tokeninfo",
            f"&contractaddress={token_id}", f"&apikey={self.API_KEY}"])

    def run_query(self, query: str):
        """Note, Etherscan restricts the token_info query to 2 calls per second.
        
        Args: 
            query (str): URL/API endpoint to query with `Requests.request.get()`
        
        Returns: 
            (dict): Component of the Requests.Response object
        """
        return super().run_query(query=query, rate_limit=True)
    
    def get_token_info(self, 
                       token_ids: Union[str, List[str]], 
                       save: bool = False, 
                       verbose: bool = False) -> TokenInfoMap:
        """[summary]

        Args:
            token_ids (Union[str, List[str]]): A token address or list of token
                addresses.
            save (bool): Saves the queried token info to json. 
                Defaults to False.

        Raises:
            ValueError: If 'token_ids' is not a string or list.

        Returns:
            token_info_maps (TokenInfoMap): Dict[TokenID, TokenInfo]
        """
        if not isinstance(token_ids, (str, list)):
            raise ValueError()
        if isinstance(token_ids, str):
            token_ids = [token_ids]

        token_info_maps: TokenInfoMap = {}

        for _, token_id in enumerate(token_ids):
            # Make query.
            query = self._token_info_query_url(token_id=token_id)
            response: List[Dict[str, str]] = self.run_query(query=query)
            if isinstance(response, str):
                raise Exception(response)

            # Create token info map
            token_info_map: TokenInfoMap = {token_id: response[0]}
            token_info_maps.update(token_info_map)

            if _ % 2 == 1:
                time.sleep(0.99) # Wait 1 second after 2 queries.

            if save:
                self.save_token_info_json(token_info_map=token_info_maps)
            if verbose:
                print(f"Token info gathered for {response[0]['symbol']}.")

        return token_info_maps
    
    def save_token_info_json(self, 
                             token_info_map: TokenInfoMap, 
                             save_dir: Optional[str] = None) -> None:
        """[summary] TODO docs

        Args:
            token_info_map (TokenInfoMap): [description]
        """

        filename = "token_info.json"
        if save_dir is not None:
            if not os.path.exists(save_dir):
                raise ValueError("")
            save_path = os.path.join(save_dir, filename)
        else:
            save_path = filename

        new_token_info_maps = token_info_map

        if not os.path.exists(save_path):
            token_info_json: TokenInfoMap = new_token_info_maps
        else:
            with open(file=save_path, mode='r') as f:
                current_token_info_maps: TokenInfoMap = json.load(f)
                if current_token_info_maps is None:
                    current_token_info_maps = {}
            current_token_info_maps.update(new_token_info_maps)
            token_info_json: TokenInfoMap = current_token_info_maps
            
        with open(save_path, "w") as f:
            json.dump(token_info_json, f, indent=3)