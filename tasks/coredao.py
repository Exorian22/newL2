import asyncio
import random
from typing import Optional

import web3
from web3.types import TxParams
from web3.contract import AsyncContract
from eth_typing import ChecksumAddress

from tasks.base import Base
from eth_async.models import TxArgs, TokenAmount, Networks, Network
from eth_async.client import Client
from data.models import Contracts
from eth_async.client import Client


class CoreDao(Base):
    async def send_usdt_bsc(
            self,
            amount: TokenAmount | None,
            slippage: float = 0.5,
    ):
        failed_text = f'Failed to send BSC USDT to Core via CoreBridge'
        token_address = Contracts.BSC_USDT.address
        contract_address = await self.client.contracts.get(contract_address=Contracts.BSC_COREDAO_BRIDGE)

        if not amount:
            amount = await self.client.wallet.balance(token=token_address)

        if await self.approve_interface(
            token_address=token_address,
            spender=contract_address.address,
            amount=amount
        ):
            await asyncio.sleep(random.randint(2, 5))
        else:
            return f'{failed_text} | Can not approve'

        callParams = TxArgs(
            refundAddress=self.client.account.address,
            zroPaymentAddress='0x0000000000000000000000000000000000000000'
        )

        params = TxArgs(
            token=token_address,
            amountLD=amount.Wei,
            to=self.client.account.address,
            callParams=callParams.tuple(),
            adapterParams=self.client.w3.to_bytes(text='')
        )

        value = await self.get_value(router_contract=contract_address)

        tx_params = TxParams(
            to=contract_address.address,
            data=contract_address.encodeABI('bridge', params.tuple()),
            value=value.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)

        reciept = await tx.wait_for_receipt(client=self.client, timeout=300)
        if reciept:
            return (f'{amount.Ether} USDT was send from {self.client.network.name} to Core '
                    f'via Core Bordge: {tx.hash.hex()}')
        return f'{failed_text}'



    async def get_value(self, router_contract: AsyncContract) -> TokenAmount:
        res = await router_contract.functions.estimateBridgeFee(
            True,
            '0x'
        ).call()
        return TokenAmount(amount=res[0], wei=True)


