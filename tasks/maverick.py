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

MaverickABI = {
    "inputs": [
        {
            "components": [
                {
                    "internalType": "address",
                    "name": "sender",
                    "type": "address"
                },
                {
                    "internalType": "address",
                    "name": "contract",
                    "type": "address"
                },
                {
                    "internalType": "bool",
                    "name": "ethornot",
                    "type": "bool"
                },
                {
                    "internalType": "uint256",
                    "name": "amountOut",
                    "type": "uint256"
                },
                {
                    "internalType": "uint256",
                    "name": "amountIn",
                    "type": "uint256"
                }
            ],
            "internalType": "struct ISlimRouter.ExactInputSingleParams",
            "name": "params",
            "type": "tuple"
        }
    ],
    "name": "exactInputSingle",
    "outputs": [
        {
            "internalType": "uint256",
            "name": "amountOut",
            "type": "uint256"
        }
    ],
    "stateMutability": "payable",
    "type": "function"
}

class Maverick(Base):
    async def swap_eth_to_usdce(
            self,
            amount: TokenAmount | None = None,
            slippage: float = 1
    ):
        from_token = Contracts.ZKSYNC_ETH
        from_token_name = Contracts.ZKSYNC_ETH.title

        to_token = Contracts.ZKSYNC_USDC_E
        to_token_name = Contracts.ZKSYNC_USDC_E.title

        contract = await self.client.contracts.get(contract_address=Contracts.MAVERICK_ETH_USDCE_CONTRACT)

        failed_text = f'Failed swap {from_token_name} to {to_token_name} via Maverick'

        if not amount:
            amount = await self.client.wallet.balance(token=from_token)

        from_token_price_dollar = await self.get_token_price(token_symbol=from_token_name)
        to_token_price_dollar = await self.get_token_price(token_symbol=to_token_name)

        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * from_token_price_dollar / to_token_price_dollar * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token.address)
        )



        params = TxArgs(
            recipient=self.client.account.address,
            pool=Contracts.MAVERICK_ETH_USDCE_CONTRACT.address,
            tokenAIn=False,
            amountIn=amount.Wei,
            amountOutMinimum=amount_out_min.Wei
        )




        tx_params = TxParams(
            to='0xad8262e847676E7eDdAFEe664c4fd492789260ba',
            data=contract.encodeABI('exactInputSingle', args=params.tuple()),
            value=amount.Wei
        )




        print(tx_params)
        return


        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)

        if receipt:
            return f'{amount.Ether} {from_token_name} was swapped to {to_token_name} via Maverick: {tx.hash.hex()}'
        return f'{failed_text}'






'''usdce - eth
0.013134 - 0.00001399080225 eth


0xa3b105ca

000000000000000000000000f9abf2a96174e8a1f35900167463298476dc58a2 addres
000000000000000000000000621c665730ee87e1425dbdd3a2de54ad29fc9de0
0000000000000000000000000000000000000000000000000000000000000001
000000000000000000000000000000000000000000000000000000000000334e amountout(сколько плачу)
000000000000000000000000000000000000000000000000000003f7c1210bfd amount in(получаю)

eth-usdce
0.000025100406 - 0.013134 usdc

0xa3b105ca
000000000000000000000000f9abf2a96174e8a1f35900167463298476dc58a2
00000000000000000000000028c0f5f11b1ac009239b0ca474c47c404f877068
0000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000400746fe000
00000000000000000000000000000000000000000000000000000000000032cc
{
    "func": "exactInputSingle",
    "params": [
        "0x0672aFFDd7d9AD1bf2BaEC30310e53A063A71CB2",
        "0x621C665730ee87e1425dBDd3a2DE54aD29Fc9DE0",
        false,
        10000000000000,
        29594
    ]
}

0xa3b105ca
0000000000000000000000000672affdd7d9ad1bf2baec30310e53a063a71cb2
000000000000000000000000621c665730ee87e1425dbdd3a2de54ad29fc9de0
0000000000000000000000000000000000000000000000000000000000000000
000000000000000000000000000000000000000000000000000009184e72a000
000000000000000000000000000000000000000000000000000000000000739a

'''