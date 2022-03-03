#!/usr/bin/env python

from typing import TypedDict

class TxReceipt(TypedDict):
    """An Ethereum transaction receipt from the Etherscan API.

    Keys (value_type): 
        effectiveGasPrice (int): Gas price at the time of the transaction. 
            A base 16 encoded integer units of Wei.
        gasUsed (int): Gas usage by the transaction. A base 16 encoded integer
            in units of Wei. Thus, `int(gasUsed, base=16)` is an integer.  
        cumulativeGasUsed (int): TODO description
        from: Address the transaction was sent from.
        to: 
        blockHash: Any
        blockNumber: Any
        contractAddress: Any
        logs: dict
        logsBloom: Any
        status: Any
        transactionHash: Any 
        transactionIndex: Any
        type: Any
    """

class NormalTx(TypedDict):
    """An Etherscan "normal" transaction performed by an address.

    blockHash (str):
    blockNumber (str): The block number that the transaction was included in.
    confirmations (str):
    contractAddress (str):
    cumulativeGasUsed (str):
    from (str): The account that originally sent the transaction.
    gas (str):
    gasPrice (str): The amount of Ether per unit of gas payed for the 
        transaction. Denoted in units of ... (=1e... Ether). TODO:
    gasUsed (str): Gas usage by the transaction. A base 16 encoded integer
        in units of Wei. Thus, `int(gasUsed, base=16)` is an integer.
    hash (str): A unique identifier for the transaction.
    input (str): Short for input data. Information that is passed to a smart 
        contract when a transaction is sent to its address. However, if the 
        transaction is creating a contract, the contract’s bytecode is placed in 
        the 'input' field.
    isError (str):
    nonce (str): The count of transactions sent out of the account. The number 
        is initialized at 0 and is incremented by 1 for each transaction sent.
    timeStamp (str): The time that the block was mined in UTC.
    to (str): The account that the transaction is addressed to.
    transactionIndex (str):
    txreceipt_status (str):
    value (str): The amount of Ether included in the transaction.
    """

class InternalMsgCall(TypedDict):
    """An Ethereum internal message call. Interanl message calls, also called 
    "internal transactions" are value transfers that were initiated by executing 
    a contract. 
    
    Despite the alternate name, internal transactions (which isn't part of the 
    yellowpaper yet still became a convention), internal transactions aren't 
    actual transactions. They're the effects of running some transaction in 
    question on the blockchain state. 
    
    In other words, internal transactions aren't included or stored on the 
    blockchain. Blockchain explorers like etherscan obtain them by 
    running a modified node with an instrumented EVM, which record all the value 
    transfers that took place as part of transaction execution, storing them 
    separately.

    Ref: 
    - Nick Johnson. 2016. https://ethereum.stackexchange.com/a/3427
    - eth. 2016. https://ethereum.stackexchange.com/a/6477
    """