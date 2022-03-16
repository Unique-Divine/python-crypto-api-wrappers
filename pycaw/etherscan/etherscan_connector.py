import os
import time
import logging
import pandas as pd

import requests

from pycaw import eth
from pycaw.etherscan import types
from typing import Any, Dict, List, Optional, TypedDict, Union


class EtherscanConnector:

    api_endpoint_preamble = "https://api.etherscan.io/api?"
    API_KEY = os.environ['ETHERSCAN_API_KEY']

    def __init__(self, max_api_calls_sec: int = 30):
        self._api_call_sleep_time = 1 / max_api_calls_sec

    def _rate_limit(self) -> None:
        time.sleep(self._api_call_sleep_time)

    @staticmethod
    def _validate_timestamp_format(self, 
                                   timestamp: Union[int, str, pd.Timestamp]):
        raise NotImplementedError() # TODO
    
    def run_query(self, query: str, rate_limit: bool = True) -> Dict[str, Any]:
        """Func is wrapped with some ultimate limiters to ensure this method is 
        never callled too much.  However, the batch-call function should also 
        limit itself, since it is likely to have a higher-level awareness (at 
        least passed in by the caller) as to how the rate itself should be 
        spread across different token-pairs

        Args: 
            query (str): URL/API endpoint to query with Requests.request.get()

        Returns:
            (dict): Component of the requests.Response object
        """
        # TODO: Parse response to see if the rate-limit has been hit
        headers = {'Content-Type': 'application/json'}
        try:
            response: requests.Response = requests.get(query, headers=headers)
            
            if not (response and response.ok):
                msg = (f"Failed request with status code {response.status_code}"
                       + f": {response.text}")
                logging.warning(msg)
                raise Exception(msg)

            if rate_limit:
                self._rate_limit()
            return response.json()['result']
        except Exception:
            logging.exception(f"Problem in query: {query}")
            # Raise so retry can retry
            raise

    def get_tx_receipt(self, tx_hash: str) -> types.TxReceipt:
        tx_receipt_url = "".join([
            self.api_endpoint_preamble, "module=proxy", 
            "&action=eth_getTransactionReceipt", "&txhash={transaction_hash}", 
            "&apikey={api_key}"])

        tx_receipt_query = tx_receipt_url.format(
            transaction_hash=tx_hash, api_key=self.API_KEY)
        tx_receipt: types.TxReceipt = self.run_query(tx_receipt_query)
        return tx_receipt

    def get_event_log(self, address: str, topic0: str) -> Dict[str, Any]:
        """[summary]

        Args:
            address (str): A 20 byte Ethereum address.
            topic0 (str): [description]

        Returns:
            [dict]: [description]
        
        References: 
            API docs: https://docs.etherscan.io/api-endpoints/logs
            Ethereum docs on events: https://ethereum.org/ig/developers/tutorials/logging-events-smart-contracts/
        """
        event_log_url: List[str] = [
            self.api_endpoint_preamble, "module=logs&", "action=getLogs&", 
            "address={address}&", "topic0={topic0}&", "apikey={api_key}"]
        event_log_url: str = "".join(event_log_url)

        event_log_query = event_log_url.format(
            address=address, topic0=topic0, api_key=self.API_KEY)
        return self.run_query(event_log_query)
    
    def get_normal_transactions(self, address: str) -> List[types.NormalTx]:

        api_key = self.API_KEY
        tx_list_url: str = "".join([
            self.api_endpoint_preamble, "module=account", 
            f"&action=txlist&address={address}&", f"sort=asc&apikey={api_key}"])
    
        return self.run_query(query=tx_list_url)

    
    def get_contract_abi(self, address: str) -> dict:
        contract_abi_url = "".join([
            self.api_endpoint_preamble,  "module=contract&", "action=getabi", 
            "&address={address}", "&apikey={api_key}"])
        contract_abi_query: str = contract_abi_url.format(
            address=address, api_key=self.API_KEY)
        return self.run_query(query=contract_abi_query)
    
    def get_block_number_before_timestamp(self, 
                                          timestamp: int, 
                                          closest: str = "before"
                                          ) -> Dict[str, Any]:
        """Returns the block number that was mined at a certain timestamp.

        Args:
            timestamp (int): Integer representing the Unix timestamp in seconds.
            closest (str, optional): Toggles whether to take the closest 
                available block that is before or after 'timestamp'. 
                Defaults to "after".
        
        Returns:
            (Dict[str, Any]): Response JSON with the block number that was mined 
                at a certain timestamp.

        Sample response: {
            "status":"1",
            "message":"OK",
            "result":"12712551"
            }
        
        Ref: https://docs.etherscan.io/api-endpoints/blocks#get-block-number-by-timestamp
        """
        if closest not in ["before", "after"]:
            raise ValueError("Value for 'closest' must be 'before' or 'after'.")
    
        block_number_by_ts_query: str = "".join([
            self.api_endpoint_preamble, "module=block", 
            "&action=getblocknobytime", "&timestamp={timestamp}", 
            f"&closest={closest}", "&apikey={api_key}"])

        query = block_number_by_ts_query.format(timestamp=timestamp, 
                                                api_key=self.API_KEY)
        return self.run_query(query)

    def get_gas_price_daily_avg(self, startdate: str,
                                enddate: str) -> Union[list, dict]:
        """Queries the daily average gas price on the Ethereum network using the
        Etherscan API. 

        Args:
            startdate (str): Starting UTC date of the query.
            enddate (str): Ending UTC date of the query.
        """
        gas_price_daily_avg_url: List[str] = [
            "https://api.etherscan.io/api", 
            "?module=stats&action=dailyavggasprice", 
            "&startdate=__STARTDATE__", 
            "&enddate=__ENDDATE__&sort=asc"
            f"&apikey={self.API_KEY}"]
        gas_price_daily_avg_url: str = "".join(gas_price_daily_avg_url)
        gas_price_daily_avg_url = gas_price_daily_avg_url.replace(
            "__STARTDATE__", startdate).replace("__ENDDATE__", enddate)

        headers = {'Content-Type': 'application/json'}
        request = requests.get(gas_price_daily_avg_url, headers=headers)

        if request.status_code == 200:
            breakpoint()  # TODO doc for json
            return request.json()
        else:
            raise Exception(
                f'Query failed with status, {request.status_code}.{gas_price_daily_avg_url}'
            )
    
    def gas_price_current(self) -> dict:
        gas_price_current_url: List[str] = [
            self.api_endpoint_preamble, "module=gastracker", 
            "&action=gasoracle", "&apikey={api_key}"]
        gas_price_current_url: str = "".join(gas_price_current_url)
        query = gas_price_current_url.format(api_key=self.API_KEY)
        return self.run_query(query)

    def get_tx_gas_info(self, tx_hash: str) -> eth.GasInfo:
        """
        Example transaction hash:
            "0x1e2910a262b1008d0616a0beb24c1a491d78771baa54a33e66065e03b1f46bc1"
        """

        tx_receipt: types.TxReceipt = self.get_tx_receipt(tx_hash=tx_hash)
        gas_price_wei: int = int(tx_receipt["effectiveGasPrice"], base=16)
        gas_used_wei: int = int(tx_receipt["gasUsed"], base=16)

        eth_price_usd = None #  TODO 
        tx_timestamp = None 

        return eth.GasInfo(gas_used_wei=gas_used_wei, 
                           gas_price_wei=gas_price_wei, 
                           eth_price_usd=eth_price_usd, 
                           tx_hash=tx_hash, 
                           timestamp=tx_timestamp)

    def get_eth_daily_price(self, startdate: str, enddate: str):

        eth_daily_price_url: List[str] = [
            self.api_endpoint_preamble, "module=stats", "&action=ethdailyprice"
            "&startdate=__STARTDATE__", "&enddate=__ENDDATE__sort=asc", 
            f"&apikey={self.API_KEY}"]
        eth_daily_price_url: str = "".join(eth_daily_price_url)
        eth_daily_price_url = eth_daily_price_url.replace(
            "__STARTDATE__", startdate).replace("__ENDDATE__", enddate)
        
        headers = {'Content-Type': 'application/json'}
        request = requests.get(eth_daily_price_url, headers=headers)

        if not request.status_code == 200:
            raise Exception(
                f'Query failed and return code is {request.status_code}.{eth_daily_price_url}'
                )
        return request.json()