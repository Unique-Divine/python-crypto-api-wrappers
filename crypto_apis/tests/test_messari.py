import crypto_apis
from crypto_apis import data_transforms
import pandas as pd
from typing import List

#%%  Price data 

from messari import timeseries

def prices_test_query():
    assets = ['btc', 'eth']
    metric = "price"
    start = "2020-06-01"
    end = "2020-07-01"
    prices_df = timeseries.get_metric_timeseries(
        asset_slugs=assets, asset_metric=metric, start=start, end=end)
    breakpoint()
    
# prices_test_query() # It works. Now, we just need parameters.


