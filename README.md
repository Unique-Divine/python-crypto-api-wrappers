# python-crypto-api-wrappers

Python Crypto API Wrappers (`pycaw`) is a package for connecting to cryptocurrency APIs like Etherscan, Messari, CoinGecko, and Coin Market Cap.


# Setup and Installation

You'll need to add your API keys as environment variables in order to use different sections of the "crypto_apis" package. The package expects a `.env` file at the repo root to set each constant.

```bash
# Example .env file that needs to be created at the root of the repo:
ETHERSCAN_API_KEY = ""
COINMARKETCAP_API_KEY = ""
MESSARI_API_KEY = ""
FTMSCAN_API_KEY = ""
```

TODO: `set_env_vars.py` or `set_env_vars.sh`: Write a script to create the .env file for the user.

# Usage Instructions

---

## Messari

Messari sub-section is forked from [messari/messari-python-api](https://github.com/messari/messari-python-api), the official Python client for the Messari API.

Example notebooks:
- [Messari API Tutorial.ipynb][messari-api-nb-example-nbviewer]
- [DefiLlama API Tutorial.ipynb][defillama-nb-example-nbviewer]


[defillama-nb-example]: https://github.com/messari/messari-python-api/blob/master/examples/notebooks/DeFiLlama%20API%20Tutorial.ipynb
[defillama-nb-example-nbviewer]:https://nbviewer.jupyter.org/github/messari/messari-python-api/blob/master/examples/notebooks/DeFiLlama%20API%20Tutorial.ipynb

[messari-api-nb-example]: https://github.com/messari/messari-python-api/blob/master/examples/notebooks/Messari%20API%20Tutorial.ipynb
[messari-api-nb-example-nbviewer]: https://nbviewer.jupyter.org/github/messari/messari-python-api/blob/master/examples/notebooks/Messari%20API%20Tutorial.ipynb

---

TODO: .
- [ ] Usage instructions.
- [ ] pypi pip install isntructions.
- [ ] See about conda-force listing.
- [ ] Dependencies and and the requirements file
- [ ] Etherscan functions
- [ ] Messari tests
- [ ] CoinGecko

