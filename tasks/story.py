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


class Story(Base):
    async def mint_nft(self) -> str:

        # contract = await self.client.contracts.get(contract_address='0x0f00a58A741aD6C9DFb549e8B0aad1e9bC48D9f1')

        tx_params = TxParams(
            to='0x59a0B4E4074B2DB51B218A7cAb3B4F4715C8b360',
            data=f'0x40d097c3000000000000000000000000{self.client.account.address[2:]}',
            value=0
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'Sucsessefull mint: {tx.hash.hex()}'
        return f'Non mint'




