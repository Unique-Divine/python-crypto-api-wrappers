"""Leverage the Messari Python API to get historical price data."""
#%%
import os, sys
import requests
import json
import __init__
import somm_airdrop
from datetime import datetime
from typing import Dict, Optional, Set, List, Union


# TODO Clean up the script
class MessariRequest:
    """Makes API call for daily prices (open, close, high, low, volume)."""
    def __init__(self, symbols: Union[str, List[str]], start: str, end: str) -> None:
        self.symbols = symbols
        self._make_symbols_a_list()
        self.pair_dir: str = os.path.join("data", self.pair) # TODO Change save location to make sense.
        self._validate_inputs()
        ...

    def _make_symbols_a_list(self):
        if not isinstance(self.symbols, (list, str)):
            raise ValueError("'symbols' must be a string or list of strings.")
        
        if isinstance(self.symbols, str):
            self.symbols = [self.symbols]
        assert isinstance(self.symbols, list)

    def _validate_inputs(self):
        # TODO Refactor
        save_dir = self.pair_dir
        if ("data" in os.listdir()) and save_dir is None:
            save_dir: str = "data"
        elif save_dir is not None:
            assert os.path.exists(save_dir)
        else:
            raise ValueError(f"Invalid 'save_dir': {save_dir} from current " +
                             f"directory {os.getcwd()}")

    def request_price_data(self) -> Dict[str, pd.DataFrame]:
        """Queries the latest flipside swaps or LP actions tables.

        Returns:
            List[dict]: [description]
        """

        # There's no API request. Use your code from notebook.py
        response: requests.Response = requests.get(url)

        if response.status_code == 200:
            return response.json()  # TODO return type? -> Create TypedDict
        else:
            raise Exception('Get request failed. Status code {}'.format(
                response.status_code))


def main():
    ... 


if __name__ == "__main__":
    # main()

