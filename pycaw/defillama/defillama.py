"""This module is meant to contain the DeFiLlama class

DeFiLLama API Docs: https://defillama.com/docs/api
"""

import datetime

from pycaw.defillama import helpers
from pycaw.messari import dataloader
from pycaw.messari import utils

import pandas as pd
from typing import Union, List, Dict


##########################
# URL Endpoints
##########################


class DeFiLlama(dataloader.DataLoader):
    """This class is a wrapper around the DeFi Llama API"""

    api_urls: Dict[str, str]

    def __init__(self):
        messari_to_dl_dict = utils.get_taxonomy_dict("messari_to_dl.json")
        dataloader.DataLoader.__init__(
            self, api_dict=None, taxonomy_dict=messari_to_dl_dict
        )

    @property
    def api_urls(self) -> Dict[str, str]:
        _endpoint_preamble: str = "https://api.llama.fi"
        urls = dict(
            # List all protocols on defillama along with their tvl
            protocols="/".join([_endpoint_preamble, "protocols"]),
            # Get historical TVL of a protocol and breakdowns by token and chain
            get_protocol_tvl="/".join([_endpoint_preamble, "protocol", "{_slug}"]),
            # Get historical TVL on DeFi on all chains
            global_tvl="/".join([_endpoint_preamble, "charts"]),
            # Get historical TVL of a chain
            chain_tvl="/".join([_endpoint_preamble, "charts", "{_chain}"]),
            # Get current TVL of a protocol
            current_protocol_tvl="/".join([_endpoint_preamble, "tvl", "{_slug}"]),
            # Get current TVL of all chains
            all_chains_tvl="/".join([_endpoint_preamble, "chains"]),
        )
        return urls
        # TODO test: Check that the urls aren't broken now.

    def get_protocol_tvl_timeseries(
        self,
        asset_slugs: Union[str, List],
        start_date: Union[str, datetime.datetime] = None,
        end_date: Union[str, datetime.datetime] = None,
    ) -> pd.DataFrame:
        """Returns times TVL of a protocol with token amounts as a pandas DataFrame.
        Returned DataFrame is indexed by df[protocol][chain][asset].

        Parameters
        ----------
           asset_slugs: str, list
               Single asset slug string or list of asset slugs (i.e. bitcoin)

           start_date: str, datetime.datetime
               Optional start date to set filter for tvl timeseries ("YYYY-MM-DD")

           end_date: str, datetime.datetime
               Optional end date to set filter for tvl timeseries ("YYYY-MM-DD")

        Returns
        -------
           DataFrame
               pandas DataFrame of protocol TVL, indexed by df[protocol][chain][asset]
               to look at total tvl across all chains, index with chain='all'
               to look at total tvl across all tokens of a chain, asset='totalLiquidityUSD'
               tokens can be indexed by asset='tokenName' or by asset='tokenName_usd'
        """
        slugs = self.translate(asset_slugs)

        slug_df_list: List = []
        for slug in slugs:
            endpoint_url = self.api_urls["get_protocol_tvl"].format(_slug=slug)
            protocol = self.get_response(endpoint_url)

            ###########################
            # This portion is basically grabbing tvl metrics on a per chain basis

            # TODO this is gonna be difficult
            chain_tvls = protocol["chainTvls"]
            chains = protocol["chains"]
            chain_list = []
            chain_df_list = []
            for chain in chains:
                chain_list.append(chain)

                # get timeseries
                chain_tvl = chain_tvls[chain]["tvl"]
                chain_tvl_tokens = chain_tvls[chain]["tokens"]
                chain_tvl_tokens_usd = chain_tvls[chain]["tokensInUsd"]

                # convert tokens & tokensInUsd
                for token in chain_tvl_tokens:
                    for key, value in token["tokens"].items():
                        token[key] = value
                    token.pop("tokens", None)

                for token in chain_tvl_tokens_usd:
                    for key, value in token["tokens"].items():
                        token[key] = value
                    token.pop("tokens", None)

                # convert to df
                chain_tvl_df = pd.DataFrame(chain_tvl)
                chain_tvl_tokens_df = pd.DataFrame(chain_tvl_tokens)
                chain_tvl_tokens_usd_df = pd.DataFrame(chain_tvl_tokens_usd)

                # fix indexes
                chain_tvl_df = helpers.format_df(chain_tvl_df)
                chain_tvl_tokens_df = helpers.format_df(chain_tvl_tokens_df)
                chain_tvl_tokens_usd_df = helpers.format_df(chain_tvl_tokens_usd_df)
                chain_tvl_tokens_usd_df = chain_tvl_tokens_usd_df.add_suffix("_usd")

                # concat tokens and tokensInUsd
                joint_tokens_df = pd.concat(
                    [chain_tvl_tokens_df, chain_tvl_tokens_usd_df], axis=1
                )
                # Join total chain TVL w/ token TVL
                chain_df = chain_tvl_df.join(joint_tokens_df)
                chain_df_list.append(chain_df)

            ###########################
            # This portion is basically grabbing tvl metrics for all chains combined

            ######################################
            # Get protocol token balances

            ## tokens in native amount
            tokens = protocol["tokens"]
            for token in tokens:
                for key, value in token["tokens"].items():
                    token[key] = value
                token.pop("tokens", None)
            tokens_df = pd.DataFrame(tokens)
            tokens_df = helpers.format_df(tokens_df)

            ## tokens in USD
            tokens_usd = protocol["tokensInUsd"]
            for token in tokens_usd:
                for key, value in token["tokens"].items():
                    token[key] = value
                token.pop("tokens", None)
            tokens_usd_df = pd.DataFrame(tokens_usd)
            tokens_usd_df = helpers.format_df(tokens_usd_df)
            tokens_usd_df = tokens_usd_df.add_suffix("_usd")

            # Get total tvl across chains
            tvl = protocol["tvl"]
            total_tvl_df = pd.DataFrame(tvl)
            total_tvl_df = helpers.format_df(total_tvl_df)

            # Working
            joint_tokens_df = pd.concat([tokens_df, tokens_usd_df], axis=1)
            total_df = total_tvl_df.join(joint_tokens_df)

            # Now create multi index
            chain_list.append("all")
            chain_df_list.append(total_df)

            slug_df = pd.concat(chain_df_list, keys=chain_list, axis=1)
            slug_df_list.append(slug_df)

        total_slugs_df = pd.concat(slug_df_list, keys=slugs, axis=1)
        total_slugs_df.sort_index(inplace=True)

        total_slugs_df = utils.time_filter_df(
            total_slugs_df, start_date=start_date, end_date=end_date
        )
        return total_slugs_df

    def get_global_tvl_timeseries(
        self,
        start_date: Union[str, datetime.datetime] = None,
        end_date: Union[str, datetime.datetime] = None,
    ) -> pd.DataFrame:
        """Returns timeseries TVL from total of all Defi Llama supported protocols

        Parameters
        ----------
           start_date: str, datetime.datetime
               Optional start date to set filter for tvl timeseries ("YYYY-MM-DD")

           end_date: str, datetime.datetime
               Optional end date to set filter for tvl timeseries ("YYYY-MM-DD")

        Returns
        -------
           DataFrame
               DataFrame containing timeseries tvl data for every protocol
        """
        global_tvl = self.get_response(self.api_urls["global_tvl"])
        global_tvl_df = pd.DataFrame(global_tvl)
        global_tvl_df = helpers.format_df(global_tvl_df)
        global_tvl_df = utils.time_filter_df(
            global_tvl_df, start_date=start_date, end_date=end_date
        )
        return global_tvl_df

    def get_chain_tvl_timeseries(
        self,
        chains_in: Union[str, List],
        start_date: Union[str, datetime.datetime] = None,
        end_date: Union[str, datetime.datetime] = None,
    ) -> pd.DataFrame:
        """Retrive timeseries TVL for a given chain

        Parameters
        ----------
           chains_in: str, list
               Single asset slug string or list of asset slugs (i.e. bitcoin)

           start_date: str, datetime.datetime
               Optional start date to set filter for tvl timeseries ("YYYY-MM-DD")

           end_date: str, datetime.datetime
               Optional end date to set filter for tvl timeseries ("YYYY-MM-DD")

        Returns
        -------
           DataFrame
               DataFrame containing timeseries tvl data for each chain
        """
        chains = utils.validate_input(chains_in)

        chain_df_list = []
        for chain in chains:
            endpoint_url = self.api_urls["chain_tvl"].format(_chain=chain)
            response = self.get_response(endpoint_url)
            chain_df = pd.DataFrame(response)
            chain_df = helpers.format_df(chain_df)
            chain_df_list.append(chain_df)

        # Join DataFrames from each chain & return
        chains_df = pd.concat(chain_df_list, axis=1)
        chains_df.columns = chains
        chains_df = utils.time_filter_df(
            chains_df, start_date=start_date, end_date=end_date
        )
        return chains_df

    def get_current_tvl(self, asset_slugs: Union[str, List]) -> Dict:
        """Retrive current protocol tvl for an asset

        Parameters
        ----------
           asset_slugs: str, list
               Single asset slug string or list of asset slugs (i.e. bitcoin)

        Returns
        -------
           DataFrame
               Pandas Series for tvl indexed by each slug {slug: tvl, ...}
        """
        slugs = utils.validate_input(asset_slugs)

        tvl_dict = {}
        for slug in slugs:
            endpoint_url = self.api_urls["current_protocol_tvl"].format(_slug=slug)
            tvl = self.get_response(endpoint_url)
            if isinstance(tvl, float):
                tvl_dict[slug] = tvl
            else:
                print(f"ERROR: slug={slug}, MESSAGE: {tvl['message']}")

        tvl_series = pd.Series(tvl_dict)
        tvl_df = tvl_series.to_frame("tvl")
        return tvl_df

    def get_protocols(self) -> pd.DataFrame:
        """Returns basic information on all listed protocols, their current TVL
        and the changes to it in the last hour/day/week

        Returns
        -------
        DataFrame
           DataFrame with one column per DeFi Llama supported protocol
        """
        protocols = self.get_response(self.api_urls["protocols"])

        protocol_dict = {}
        for protocol in protocols:
            protocol_dict[protocol["slug"]] = protocol

        protocols_df = pd.DataFrame(protocol_dict)
        return protocols_df
