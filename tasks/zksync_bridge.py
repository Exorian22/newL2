import asyncio
import sys
from typing import Optional
from web3.types import TxParams
import time
import random
import json

from web3 import Web3
from web3.eth import AsyncEth
from fake_useragent import UserAgent
import requests

from eth_async.models import TxArgs, TokenAmount
from eth_async.client import Client
from eth_async import transactions
from eth_async import types
from eth_async.models import RawContract, TokenAmount
from eth_async.client import Client
from data.models import Contracts
from tasks.base import Base
from eth_async.wallet import Wallet


class ZkSyncBridge(Base):
    async def bridge_eth_to_zk(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 0.5,
    ):

        failed_text = f'Failed to send ETH from Ethereum to ZkSync via ZkSync Bridge'

        from_token = await self.client.contracts.default_token(contract_address=Contracts.ETHEREUM_ETH)
        from_token_name = Contracts.ETHEREUM_ETH.title

        to_token = await self.client.contracts.default_token(contract_address=Contracts.ZKSYNC_ETH)
        to_token_name = Contracts.ZKSYNC_ETH

        if not amount:
            amount = await self.client.wallet.balance(token=from_token.address)

        contract = await self.client.contracts.get(contract_address=Contracts.BRIDGE_ETH_TO_ZKSYNC)

        params = TxArgs(
            _contractL2=self.client.account.address,
            _l2Value=amount.Wei,
            _calldata='',
            _l2GasLimit=...,
            _gasPricePerPubdata=...,
            _factoryDeps='',
            _refundRecipient=self.client.account.address
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('requestL2Transaction', params.tuple()),
            value=amount.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)

        reciept = await tx.wait_for_receipt(client=self.client, timeout=300)
        if reciept:
            return (f'{amount.Ether} ETH was send from {self.client.network.name} to ZkSync '
                    f'via Zksync Bridge: {tx.hash.hex()}')
        return f'{failed_text}'