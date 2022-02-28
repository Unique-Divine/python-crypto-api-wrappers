# SOURCE: https://towardsdatascience.com/decoding-ethereum-smart-contract-data-eed513a65f76

import sys
import eth_utils
import functools
import web3
import web3.auto
import json
import hexbytes
from web3._utils import events 
from typing import Any, Dict, Mapping, Union
from collections.abc import Sequence

def decode_tuple(t: Union[tuple, bytes, bytearray], target_field):
    output = dict()
    for i in range(len(t)):
        if isinstance(t[i], (bytes, bytearray)):
            output[target_field[i]['name']] = eth_utils.to_hex(t[i])
        elif isinstance(t[i], (tuple)):
            output[target_field[i]['name']] = decode_tuple(
                t[i], target_field[i]['components'])
        else:
            output[target_field[i]['name']] = t[i]
    return output


def decode_list_tuple(l, target_field):
    output = l
    for i in range(len(l)):
        output[i] = decode_tuple(l[i], target_field)
    return output


def decode_list(l):
    output = l
    for i in range(len(l)):
        if isinstance(l[i], (bytes, bytearray)):
            output[i] = eth_utils.to_hex(l[i])
        else:
            output[i] = l[i]
    return output


def convert_to_hex(arg: Union[Sequence, bytes, bytearray], target_schema):
    """Convert byte codes into human-readable and json-serializable data structures
    """
    output = dict()
    for k in arg:
        if isinstance(arg[k], (bytes, bytearray)):
            output[k] = eth_utils.to_hex(arg[k])
        elif isinstance(arg[k], (list)) and len(arg[k]) > 0:
            target = [
                a for a in target_schema if 'name' in a and a['name'] == k][0]
            if target['type'] == 'tuple[]':
                target_field = target['components']
                output[k] = decode_list_tuple(arg[k], target_field)
            else:
                output[k] = decode_list(arg[k])
        elif isinstance(arg[k], (tuple)):
            target_field = [a['components'] for a in target_schema
                            if 'name' in a and a['name'] == k][0]
            output[k] = decode_tuple(arg[k], target_field)
        else:
            output[k] = arg[k]
    return output


@functools.lru_cache(maxsize=None)
def _get_contract(address, abi):
    """
    This helps speed up execution of decoding across a large dataset by caching the contract object
    It assumes that we are decoding a small set, on the order of thousands, of target smart contracts
    """
    if isinstance(abi, (str)):
        abi = json.loads(abi)

    contract = web3.auto.w3.eth.contract(
        address=web3.Web3.toChecksumAddress(address), abi=abi)
    return (contract, abi)


def decode_tx(address, input_data, abi):
    if abi is not None:
        try:
            (contract, abi) = _get_contract(address, abi)
            func_obj, func_params = contract.decode_function_input(input_data)
            target_schema = [
                a['inputs'] for a in abi if 'name' in a and a['name'] == func_obj.fn_name][0]
            decoded_func_params = convert_to_hex(func_params, target_schema)
            return (func_obj.fn_name, json.dumps(decoded_func_params), json.dumps(target_schema))
        except:
            e = sys.exc_info()[0]
            return ('decode error', repr(e), None)
    else:
        return ('no matching abi', None, None)


LogTopic = str
EventABI = Dict[LogTopic, Any]

def _get_topic2abi(abi: Union[str, EventABI]) -> Mapping[bytes, LogTopic]:
    if isinstance(abi, (str)):
        abi = json.loads(abi)
    
    event_abi: EventABI = [a for a in abi if a['type'] == 'event']
    topic2abi: Dict[bytes, LogTopic] = {
        eth_utils.event_abi_to_log_topic(topic): topic for topic in event_abi}
    return topic2abi


@functools.lru_cache(maxsize=None)
def _get_hex_topic(t):
    hex_t = hexbytes.HexBytes(t)
    return hex_t


def decode_log(data, topics, abi):
    if abi is not None:
        topic2abi = _get_topic2abi(abi)
        log = {
            'address': None,  # web3.Web3.toChecksumAddress(address),
            'blockHash': None,  # HexBytes(blockHash),
            'blockNumber': None,
            'data': data,
            'logIndex': None,
            'topics': [_get_hex_topic(_) for _ in topics],
            'transactionHash': None,  # HexBytes(transactionHash),
            'transactionIndex': None
        }
        event_abi = topic2abi[log['topics'][0]]
        evt_name = event_abi['name']

        data = events.get_event_data(web3.auto.w3.codec, event_abi, log)['args']
        target_schema = event_abi['inputs']
        decoded_data = convert_to_hex(data, target_schema)

        return (evt_name, json.dumps(decoded_data), json.dumps(target_schema))

    else:
        return ('no matching abi', None, None)
