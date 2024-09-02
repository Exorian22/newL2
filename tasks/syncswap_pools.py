import asyncio
import sys
from typing import Optional
from web3.types import TxParams
import web3
import time
import random
import json

from web3 import Web3
from web3.eth import AsyncEth
from fake_useragent import UserAgent
import requests
from decimal import Decimal

from eth_async.models import TxArgs, TokenAmount
from eth_async.client import Client
from eth_async import transactions
from eth_async import types
from eth_async.models import RawContract, TokenAmount, CommonValues
from eth_async.client import Client
from data.models import Contracts
from tasks.base import Base
from eth_async.wallet import Wallet


# class SyncSwapPools(Base):
#     async def add_liqudity_to_zk_eth_pool(
#             self,
#             amount: TokenAmount | None = None,
#     ):
#         first_toke = Contracts.ZKSYNC_ZK
#         second_token = Contracts.ZKSYNC_ETH
#
#         pool = Contracts.SYNCSWAP_LIQUDITY_POOL_ZK_ETH
#
#         contract = '0x9B5def958d0f3b6955cBEa4D5B7809b2fb26b059'
#
#
#         num = TokenAmount(amount.Ether / Decimal('169.2'))
#
#         eth_amount = TokenAmount(amount.Ether * Decimal('0.000048'))
#
#         if await self.approve_interface(
#                 token_address=Contracts.ZKSYNC_ZK.address,
#                 spender=contract,
#                 amount=amount
#         ):
#             await asyncio.sleep(random.randint(5, 10))
#         else:
#             return f' | can not approve'
#
#         data = (f'0xeb1432f0'
#                  f'{Contracts.SYNCSWAP_LIQUDITY_POOL_ZK_ETH.address.lower()[2:].zfill(64)}'
#                  f'{"e0".zfill(64)}'
#                  f'{"1c0".zfill(64)}'
#                  f'{hex(num.Wei)[2:].zfill(64)}'
#                  f'{"".zfill(64)}'
#                  f'{"200".zfill(64)}'
#                  f'{"".zfill(64)}'
#                  f'{"2".zfill(64)}'
#                  f'{Contracts.ZKSYNC_ZK.address.lower()[2:].zfill(64)}'
#                  f'{hex(amount.Wei)[2:].zfill(64)}'
#                  f'{"1".zfill(64)}'
#                  f'{"".zfill(64)}'
#                  f'{hex(eth_amount.Wei)[2:].zfill(64)}'
#                  f'{"1".zfill(64)}'
#                  f'{"20".zfill(64)}'
#                  f'{self.client.account.address.lower()[2:].zfill(64)}'
#                  f'{"".zfill(64)}'
#         )
#
#         # params = TxArgs(
#         #     pool=Contracts.SYNCSWAP_LIQUDITY_POOL_ZK_ETH.address,
#         #     path=[
#         #         (
#         #         Contracts.ZKSYNC_ZK.address,
#         #         amount.Wei,
#         #         "0x0000000000000000000000000000000000000001"
#         #      ),
#         #     (
#         #         '0x0000000000000000000000000000000000000000',
#         #         eth_amount.Wei,
#         #         "0x0000000000000000000000000000000000000001"
#         #     )
#         #         ],
#         #     address=b"000000000000000000000000f9abf2a96174e8a1f35900167463298476dc58a2",
#         #     amount1=num.Wei,
#         #     nill='0x0000000000000000000000000000000000000000',
#         #     bytes=b'0x',
#         #
#         # )
#
#
#
#
#
#
#
#         # contract2 = await self.client.contracts.get(Contracts.ZKSYNC_SYNCSWAP)
#
#
#         tx_params = TxParams(
#             to=contract,
#             data=data,
#             value=eth_amount.Wei
#         )
#
#         # print(tx_params['data'])
#         #
#         # self.parse_params_me(tx_params['data'])
#         # return
#
#         tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
#
#         receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
#         if receipt:
#             return f'Swap: {tx.hash.hex()}'
#         return f'Fail!'

class SyncSwapPools(Base):
    async def add_liquidity(
            self,
            first_token: RawContract,
            second_token: RawContract,
            first_token_amount: TokenAmount
    ):
        first_token_address = first_token.address
        second_token_address = second_token.address

        syncswap_contract = await self.client.contracts.get(
            contract_address=Contracts.ZKSYNC_SYNCSWAP_POOL,
            abi=Contracts.ZKSYNC_SYNCSWAP_POOL.abi
        )

        pool_address = await syncswap_contract.functions.getPool(
            first_token_address,
            second_token_address
        ).call()

        abi = await self.client.contracts.get_abi(contract_address=pool_address)

        pool_contract = await self.client.contracts.get(contract_address=pool_address, abi=abi)

        second_token_amount = TokenAmount(int(await pool_contract.functions.getAmountIn(
            first_token_address,
            first_token_amount.Wei,
            self.client.account.address
        ).call()), wei=True)

        totalSupply = await pool_contract.functions.totalSupply().call()
        _, reserv_second = await pool_contract.functions.getReserves().call()

        minTotalAmountIn = TokenAmount(((second_token_amount.Wei / reserv_second) * totalSupply) * 0.9, wei=True)

        router_v2_contract = await self.client.contracts.get(contract_address=Contracts.ZK_SYNCSWAP_ROUTER_V2)

        if first_token_address.upper() != Contracts.ZKSYNC_ETH.address.upper():
            if await self.approve_interface(
                    token_address=first_token_address,
                    spender=router_v2_contract.address,
                    amount=first_token_amount
            ):
                await asyncio.sleep(random.randint(1, 3))
            else:
                return f'Can not approve'
        elif second_token_address.upper() != Contracts.ZKSYNC_ETH.address.upper():
            if await self.approve_interface(
                    token_address=second_token_address,
                    spender=router_v2_contract.address,
                    amount=second_token_amount
            ):
                await asyncio.sleep(random.randint(1, 3))
            else:
                return f'Can not approve'

        if first_token_address.upper() == Contracts.ZKSYNC_ETH.address.upper():
            value = first_token_amount.Wei
        if second_token_address.upper() == Contracts.ZKSYNC_ETH.address.upper():
            value = second_token_amount.Wei
        else:
            value = 0

        inputs = [
            [
                first_token_address,
                first_token_amount.Wei,
                True
            ],
            [
                "0x0000000000000000000000000000000000000000",
                second_token_amount.Wei,
                True
            ]
        ]

        my_address = f'{str(self.client.account.address)[2:].zfill(64)}'

        params = TxArgs(
            contract=pool_contract.address,
            token=inputs,
            my_address=bytes.fromhex(my_address),
            amount=minTotalAmountIn.Wei,
            null="0x0000000000000000000000000000000000000000",
            bytes=b"",
            null2="0x0000000000000000000000000000000000000000"
        )

        tx_params = TxParams(
            to=router_v2_contract.address,
            data=router_v2_contract.encodeABI('addLiquidity2', args=params.tuple()),
            value=value
        )
        #
        # return tx_params['data']

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)


        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'Sucsess: {first_token.title} / {second_token.title} was added to pool: {tx.hash.hex()}'

        return f'Fail!'

    async def add_liquidity_zk_eth(self, first_token_amount):
        amount = TokenAmount(amount=first_token_amount, decimals=18)
        return await self.add_liquidity(
            first_token=Contracts.ZKSYNC_ZK,
            second_token=Contracts.ZKSYNC_ETH,
            first_token_amount=amount
        )

    async def add_liquidity_usdc_e_eth(self, first_token_amount):
        amount = TokenAmount(amount=first_token_amount, decimals=6)
        return await self.add_liquidity(
            first_token=Contracts.ZKSYNC_USDC_E,
            second_token=Contracts.ZKSYNC_ETH,
            first_token_amount=amount

        )

    async def withdraw_liquidity(
            self,
            first_token: RawContract,
            second_token: RawContract,
    ):

        first_token_address = first_token.address
        second_token_address = second_token.address

        syncswap_contract = await self.client.contracts.get(
            contract_address=Contracts.ZKSYNC_SYNCSWAP_POOL,
            abi=Contracts.ZKSYNC_SYNCSWAP_POOL.abi
        )

        pool_address = await syncswap_contract.functions.getPool(
            first_token_address,
            second_token_address
        ).call()

        abi = await self.client.contracts.get_abi(contract_address=pool_address)

        pool_contract = await self.client.contracts.get(contract_address=pool_address, abi=abi)

        full_amount = TokenAmount(await pool_contract.functions.balanceOf(
            self.client.account.address
        ).call(), wei=True)

        my_address = f'{str(self.client.account.address)[2:].zfill(64)}{"1".zfill(64)}'

        router_v2_contract = await self.client.contracts.get(contract_address=Contracts.ZK_SYNCSWAP_ROUTER_V2)

        totalSupply = await pool_contract.functions.totalSupply().call()
        reserv_first, reserv_second = await pool_contract.functions.getReserves().call()

        first_min = TokenAmount((full_amount.Wei * reserv_first / totalSupply) * 0.99, wei=True)
        second_min = TokenAmount((full_amount.Wei * reserv_second / totalSupply) * 0.99, wei=True)




        if await self.approve_interface(
                token_address=pool_contract.address,
                spender=router_v2_contract.address,
                amount=full_amount
        ):
            await asyncio.sleep(random.randint(1, 3))
        else:
            return f'Can not approve'

        inputs = [
            first_min.Wei,
            second_min.Wei
        ]

        args = TxArgs(
            pool=pool_contract.address,
            liquidity=full_amount.Wei,
            data=bytes.fromhex(my_address),
            minAmounts=inputs,
            callback="0x0000000000000000000000000000000000000000",
            callbackData=b"",
        )

        tx_params = TxParams(
            to=router_v2_contract.address,
            data=router_v2_contract.encodeABI('burnLiquidity', args=args.tuple()),
            value=0
        )

        # return tx_params['data']

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)

        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)

        if receipt:
            return f'Sucsess: {first_token.title} / {second_token.title} was removed from pool: {tx.hash.hex()}'

        return f'Fail!'
