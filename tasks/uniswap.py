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


class Uniswap(Base):


    # @staticmethod
    # async def get_price(amount: TokenAmount, slippage: float = 1.) -> TokenAmount:
    #
    #     headers = {
    #         'accept': '*/*',
    #         'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    #         'content-type': 'text/plain;charset=UTF-8',
    #         'origin': 'https://app.uniswap.org',
    #         'priority': 'u=1, i',
    #         'referer': 'https://app.uniswap.org/',
    #         'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    #         'sec-ch-ua-mobile': '?0',
    #         'sec-ch-ua-platform': '"Windows"',
    #         'sec-fetch-dest': 'empty',
    #         'sec-fetch-mode': 'cors',
    #         'sec-fetch-site': 'same-site',
    #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    #         'x-request-source': 'uniswap-web',
    #     }
    #
    #     data = {
    #         "tokenInChainId":42161,
    #         "tokenIn":"ETH",
    #         "tokenOutChainId":42161,
    #         "tokenOut":"0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    #         "amount":"100000000000000000",
    #         "type":"EXACT_INPUT",
    #         "intent":"quote",
    #         "configs":[
    #             {"protocols":[
    #                 "V2","V3","MIXED"
    #             ],
    #                 "routingType":"CLASSIC",
    #                 "recipient":"0x0672aFFDd7d9AD1bf2BaEC30310e53A063A71CB2"}
    #         ],
    #         "swapper":"0x0672aFFDd7d9AD1bf2BaEC30310e53A063A71CB2",
    #         "slippageTolerance":"0.5"}
    #
    #     # response = requests.post('https://interface.gateway.uniswap.org/v2/quote', headers=headers, data=data)
    #
    #     response = requests.post('https://api.uniswap.org/v2/quote', headers=headers, data=json.dumps(data))
    #     response_json = response.json()
    #
    #     quote = int(response_json['quote']['quote'])
    #     amount_with_slippage = int(quote * (100 - slippage) / 100)
    #
    #     return TokenAmount(
    #         amount=amount_with_slippage,
    #         decimals=6,
    #         wei=True
    #     )



    async def swap_eth_to_usdc(
            self,
            amount: TokenAmount,
            slippage: float = 1.,
    ) -> str:

        from_token_address = Contracts.ARBITRUM_ETH.address
        to_token_address = Contracts.ARBITRUM_USDC_e.address

        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = 'ETH'

        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = "USDC"

        failed_text = f'Failed swap {from_token_name} to {to_token_name} via Uniswap'

        contract = await self.client.contracts.get(contract_address=Contracts.ARBITRUM_UNISWAP)

        if not amount:
            amount = await self.client.wallet.balance(token=from_token)

        from_token_price_dollar = await self.get_token_price(token_symbol=from_token_name)
        to_token_price_dollar = await self.get_token_price(token_symbol=to_token_name)



        # amount_usdc = await Uniswap.get_price(amount=amount, slippage=slippage)

        amount_usdc = TokenAmount(
            amount=float(amount.Ether) * from_token_price_dollar / to_token_price_dollar * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        )



        args = TxArgs(
            commands=f'0x0b000604',
            inputs=[
                f'0x{"2".zfill(64)}{hex(amount.Wei)[2:].zfill(64)}',

                f'0x{"2".zfill(64)}'
                f'{hex(amount.Wei)[2:].zfill(64)}'
                f'{hex(amount_usdc.Wei)[2:].zfill(64)}'
                f'{"a0".zfill(64)}'
                f'{"".zfill(64)}'
                f'{"2b".zfill(64)}'
                f'82af49447d8a07e3bd95bd0d56f35241523fbab10001f4ff970a61a04b1ca14834a43f5de4533ebddb5cc8000000000000000000000000000000000000000000',

                f'0x{"ff970a61a04b1ca14834a43f5de4533ebddb5cc8".zfill(64)}'
                f'{"89f30783108e2f9191db4a44ae2a516327c99575".zfill(64)}'
                f'{"19".zfill(64)}',

                f'0x{"ff970a61a04b1ca14834a43f5de4533ebddb5cc8".zfill(64)}'
                f'{"1".zfill(64)}'
                f'{hex(amount_usdc.Wei)[2:].zfill(64)}'

        ],
            deadline=int(time.time() + 20 * 60)
        )

        print(args)


        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('execute', args=args.tuple()),
            value=amount.Wei
        )



        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'{amount.Ether} ETH was swapped to {amount_usdc.Ether} USDC: {tx.hash.hex()}'

        return f'{failed_text}!'



