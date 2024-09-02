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


class SyncSwap(Base):
    async def swap(
            self,
            from_token: RawContract,
            to_token:RawContract,
            pool:RawContract,
            amount: TokenAmount = None,
            slippage: float = 1
    ):

        from_token_symbol = from_token.title
        from_token = await self.client.contracts.default_token(contract_address=from_token.address)


        to_token_symbol = to_token.title
        to_token = await self.client.contracts.default_token(contract_address=to_token.address)



        from_token_is_eth = from_token.address.upper() == Contracts.WETH.address.upper()

        failed_text = f'Failed swap {from_token_symbol} to {to_token_symbol} via SpaceFi'
        contract = await self.client.contracts.get(contract_address=Contracts.ZKSYNC_SYNCSWAP)

        if not amount:
            amount = await self.client.wallet.balance(token=from_token.address)

        from_token_price = await self.get_token_price(token_symbol=from_token_symbol)
        to_token_price = await self.get_token_price(token_symbol=to_token_symbol)


        if not from_token_is_eth:
            if await self.approve_interface(
                    token_address=from_token.address,
                    spender=contract.address,
                    amount=amount
            ):
                await asyncio.sleep(random.randint(5, 10))
            else:
                return f'{failed_text} | can not approve'


        min_to_amount = TokenAmount(
            amount=float(amount.Ether) * from_token_price / to_token_price * (100 - slippage) / 100,
            decimals = await self.client.transactions.get_decimals(contract=to_token)
        )





        params = TxArgs(
            path=[
                TxArgs(
                    steps=[
                        TxArgs(
                            pool=pool.address,
                            data=f'0x{from_token.address[2:].zfill(64)}'
                                 f'{str(self.client.account.address)[2:].zfill(64)}'
                                 f'{("2" if from_token_is_eth else "1").zfill(64)}',
                            callback='0x0000000000000000000000000000000000000000',
                            callbackData='0x'
                        ).tuple()

                    ],
                    tokenIn='0x0000000000000000000000000000000000000000' if from_token_is_eth else from_token.address,
                    amountIn=amount.Wei

                ).tuple()

            ],
            amountOutMin=min_to_amount.Wei,
            deadline=int(time.time() + 20 * 60)
        )



        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swap', args=params.tuple()),
            value=amount.Wei if from_token_is_eth else 0
        )

        # self.parse_params_me(tx_params['data'])
        # return



        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)

        receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
        if receipt:
            return f'{amount.Ether} {from_token_symbol} was swapped to {to_token_symbol} via SyncSwap: {tx.hash.hex()}'
        return f'{failed_text}!'

    async def swap_eth_to_usdt(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1
    ) -> str:
        return await self.swap(
            from_token=Contracts.ZKSYNC_ETH,
            to_token=Contracts.ZKSYNC_USDT,
            pool=Contracts.SYNCSWAP_ETH_USDT_POOL,
            amount=amount,
            slippage=slippage
        )

    async def swap_eth_to_zk(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1
    ) -> str:
        return await self.swap(
            from_token=Contracts.ZKSYNC_ETH,
            to_token=Contracts.ZKSYNC_ZK,
            pool=Contracts.SYNCSWAP_ETH_ZK_POOL,
            amount=amount,
            slippage=slippage
        )





