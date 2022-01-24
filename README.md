# crypto-apis

You'll neeed to configure API keys in order to use various components of the repo. For now, this is done via the creation of a short Python file, `crypto_apis/secret_api_keys`, which must contain the following constants:
```python
# crypto_apis/secret_api_keys.py
ETHERSCAN_API_KEY = ""
COINMARKETCAP_API_KEY = ""
```

You'll also need to configure your Messari API key inside of the package.


## Messari

Messari sub-section is forked from [messari/messari-python-api](https://github.com/messari/messari-python-api), the official Python client for the Messari API.

Example notebooks:
- [Messari API Tutorial.ipynb][messari-api-nb-example-nbviewer]
- [DefiLlama API Tutorial.ipynb][defillama-nb-example-nbviewer]


[defillama-nb-example]: https://github.com/messari/messari-python-api/blob/master/examples/notebooks/DeFiLlama%20API%20Tutorial.ipynb
[defillama-nb-example-nbviewer]:https://nbviewer.jupyter.org/github/messari/messari-python-api/blob/master/examples/notebooks/DeFiLlama%20API%20Tutorial.ipynb

[messari-api-nb-example]: https://github.com/messari/messari-python-api/blob/master/examples/notebooks/Messari%20API%20Tutorial.ipynb
[messari-api-nb-example-nbviewer]: https://nbviewer.jupyter.org/github/messari/messari-python-api/blob/master/examples/notebooks/Messari%20API%20Tutorial.ipynb

