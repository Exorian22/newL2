import asyncio
import sys
from typing import Optional
from web3.types import TxParams
import time
import random

from web3 import Web3
from web3.eth import AsyncEth

from eth_async.models import TxArgs, TokenAmount
from eth_async.client import Client
from eth_async import transactions
from eth_async import types
from eth_async.models import RawContract, TokenAmount
from eth_async.client import Client
from data.models import Contracts
from tasks.base import Base
from eth_async.wallet import Wallet

class SpaceFi(Base):
#     async def _swap_eth_to_usdt(self, amount: TokenAmount, slippage: float = 1) -> str:
#         failed_text = "Failed swap ETH to USDT via SpaceFi"
#         contract = await self.client.contracts.get(contract_address=Contracts.ZKSYNC_SPACEFI)
#         from_token = Contracts.ZKSYNC_ETH
#         to_token = Contracts.ZKSYNC_USDT
#         eth_price = await self.get_token_price("ETH", "USDT")
#         min_to_amount = TokenAmount(
#             amount=eth_price * float(amount.Ether) * (1 - slippage / 100),
#             decimals=await self.client.transactions.get_decimals(contract=to_token.address)
#         )
#         deadline = int(time.time() + 20 * 60)
#         args = TxArgs(
#             amountOut=min_to_amount.Wei,
#             path=[
#                 from_token.address,
#                 to_token.address
#             ],
#             to=self.client.account.address,
#             deadline=deadline
#         )
#         tx_params = TxParams(
#             to=contract.address,
#             data=contract.encodeABI('swapETHForExactTokens', args=args.tuple()),
#             value=amount.Wei
#         )
#         tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
#         receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
#         if receipt:
#             return f'{amount.Ether} ETH was swaped to {min_to_amount.Ether} USDT via WooFi: {tx.hash.hex()}'
#         return f'{failed_text}!'
#
# #_____________________________________________________________________________________________________________________
#     async def _swap_eth_to_usdc(self, amount: TokenAmount, slippage: float = 1) -> str:
#
#         failed_text = "Failed swap ETH to USDC via SpaceFi"
#         contract = await self.client.contracts.get(contract_address=Contracts.ZKSYNC_SPACEFI)
#
#         from_token = Contracts.ZKSYNC_ETH
#         mid_token = Contracts.ZKSYNC_USDC_E
#         to_token = Contracts.ZKSYNC_USDC
#
#         eth_price = await self.get_token_price("ETH", "USDC")
#         min_to_amount = TokenAmount(
#             amount=eth_price * float(amount.Ether) * (1 - slippage / 100),
#             decimals=await self.client.transactions.get_decimals(contract=mid_token.address)
#         )
#
#         deadline = int(time.time() + 20 * 60)
#
#         args = TxArgs(
#             amountOut=min_to_amount.Wei,
#             path=[
#                 from_token.address,
#                 mid_token.address,
#                 to_token.address
#             ],
#             to=self.client.account.address,
#             deadline=deadline
#         )
#
#         tx_params = TxParams(
#             to=contract.address,
#             data=contract.encodeABI('swapETHForExactTokens', args=args.tuple()),
#             value=amount.Wei
#         )
#
#         tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
#         receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
#
#         if receipt:
#             return f'{amount.Ether} ETH was swaped to {min_to_amount.Ether} USDC via WooFi: {tx.hash.hex()}'
#         return f'{failed_text}!'
# #_____________________________________________________________________________________________________________________
#     async def _swap_eth_to_wbtc(self, amount: TokenAmount, slippage: float = 1) -> str:
#
#         failed_text = "Failed swap ETH to WBTC via SpaceFi"
#         contract = await self.client.contracts.get(contract_address=Contracts.ZKSYNC_SPACEFI)
#
#         from_token = Contracts.ZKSYNC_ETH
#         to_token = Contracts.ZKSYNC_WBTC
#
#         eth_price = await self.get_token_price("ETH", "BTC")
#         min_to_amount = TokenAmount(
#             amount=eth_price * float(amount.Ether) * (1 - slippage / 100),
#             decimals=await self.client.transactions.get_decimals(contract=to_token.address)
#         )
#
#         deadline = int(time.time() + 20 * 60)
#
#         args = TxArgs(
#             amountOut=min_to_amount.Wei,
#             path=[
#                 from_token.address,
#                 to_token.address
#             ],
#             to=self.client.account.address,
#             deadline=deadline
#         )
#
#         tx_params = TxParams(
#             to=contract.address,
#             data=contract.encodeABI('swapETHForExactTokens', args=args.tuple()),
#             value=amount.Wei
#         )
#
#         tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
#         receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
#
#         if receipt:
#             return f'{amount.Ether} ETH was swaped to {min_to_amount.Ether} WBTC via WooFi: {tx.hash.hex()}'
#         return f'{failed_text}!'
# #_________________________________________________________________________________________________________________
#     async def _swap_usdt_to_eth(self, amount: TokenAmount, slippage: float = 1) -> str:
#
#         failed_text = "Failed swap USDT to ETH via SpaceFi"
#         contract = await self.client.contracts.get(contract_address=Contracts.ZKSYNC_SPACEFI)
#
#         from_token = Contracts.ZKSYNC_USDT
#         to_token = Contracts.ZKSYNC_ETH
#
#
#         await self.approve_interface(token_address=from_token.address, spender=contract.address, amount=amount)
#         await asyncio.sleep(5)
#
#         eth_price = await self.get_token_price("ETH", "USDT")
#         min_to_amount = TokenAmount(
#             amount=float(amount.Ether) / eth_price * (1 - slippage / 100),
#             decimals=await self.client.transactions.get_decimals(contract=to_token.address)
#         )
#         print(min_to_amount)
#
#         deadline = int(time.time() + 20 * 60)
#
#         args = TxArgs(
#             amountIn=amount.Wei,
#             amountOutMin=min_to_amount.Wei,
#             path=[
#                 from_token.address,
#                 to_token.address
#             ],
#             to=self.client.account.address,
#             deadline=deadline
#         )
#
#         tx_params = TxParams(
#             to=contract.address,
#             data=contract.encodeABI('swapExactTokensForETH', args=args.tuple()),
#         )
#
#         # if await self.approve_interface(
#         #     token_address=from_token.address,
#         #     spender=contract.address,
#         #     amount=amount
#         # ):
#         #     await asyncio.sleep(random.randint(5, 10))
#         # else:
#         #     return f'{failed_text} | can not approve'
#
#         tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
#         receipt = await tx.wait_for_receipt(client=self.client, timeout=200)
#
#         if receipt:
#             return f'{amount.Ether} USDT was swaped to {min_to_amount.Ether} ETH via WooFi: {tx.hash.hex()}'
#         return f'{failed_text}!'

    async def _swap(
            self,
            path: list[str],
            amount: TokenAmount | None = None,
            slippage: float = 1.,
    ) -> str:
        from_token_address = Web3.to_checksum_address(path[0])
        to_token_address = Web3.to_checksum_address(path[-1])
        from_token_is_eth = from_token_address.upper() == Contracts.WETH.address.upper()

        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        failed_text = f'Failed swap {from_token_name} to {to_token_name} via SpaceFi'

        contract = await self.client.contracts.get(contract_address=Contracts.ZKSYNC_SPACEFI)

        if not amount:
            amount = await self.client.wallet.balance(token=from_token)


        # print(amount)
        # #
        # sys.exit()

        if not from_token_is_eth:
            if await self.approve_interface(
                token_address=from_token.address,
                spender=contract.address,
                amount=amount
            ):
                await asyncio.sleep(random.randint(5, 10))
            else:
                return f'{failed_text} | can not approve'

        from_token_price_dollar = await self.get_token_price(token_symbol=from_token_name)
        to_token_price_dollar = await self.get_token_price(token_symbol=to_token_name)

        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * from_token_price_dollar / to_token_price_dollar * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        )

        # print(amount.Ether)
        # print(amount.Wei)
        # print(amount_out_min)
        # print(amount_out_min.Ether)
        # print(amount_out_min.Wei)
        # # sys.exit()

        if from_token_is_eth:
            params = TxArgs(
                amountOut=amount_out_min.Wei,
                path=path,
                toAdress=self.client.account.address,
                deadline=int(time.time() + 20 * 60),
            )
        else:
            params = TxArgs(
                amountIn=amount.Wei,
                amountOutMin=amount_out_min.Wei,
                path=path,
                to=self.client.account.address,
                deadline=int(time.time() + 20 * 60),
            )

        if from_token_is_eth:
            function_name = 'swapExactETHForTokens'
        else:
            function_name = 'swapExactTokensForETH'

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI(function_name, args=params.tuple()),
            value=amount.Wei if from_token_is_eth else 0
        )
        balance = await self.client.wallet.balance(
            token=to_token.address,
            address=self.client.account.address,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        )
        # print(params)
        # print(tx_params)




        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)

        if receipt:
            return f'{amount.Ether} {from_token_name} was swapped to {to_token_name} via SpaceFi: {tx.hash.hex()}'
        return f'{failed_text}'

    async def swap_eth_to_usdt(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.,
    ):
        return await self._swap(
            amount=amount,
            path=[Contracts.WETH.address, Contracts.ZKSYNC_USDT.address],
            slippage=slippage
        )

    async def swap_usdt_to_eth(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.,
    ):
        return await self._swap(
            amount=amount,
            path=[Contracts.ZKSYNC_USDT.address, Contracts.WETH.address],
            slippage=slippage
        )

    async def swap_eth_to_usdc(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1.,
    ):
        return await self._swap(
            amount=amount,
            path=[Contracts.ZKSYNC_ETH.address, Contracts.ZKSYNC_USDC_E.address, Contracts.ZKSYNC_USDC.address]
        )