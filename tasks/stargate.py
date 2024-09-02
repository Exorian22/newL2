import asyncio
import random
from typing import Optional
from web3.types import TxParams
from web3.contract import AsyncContract
from eth_typing import ChecksumAddress

from tasks.base import Base
from eth_async.models import TxArgs, TokenAmount, Networks, Network
from eth_async.client import Client
from data.models import Contracts

class Stargate(Base):
    contract_data = {
        Networks.Arbitrum.name: {
            'usdc_contract': Contracts.ARBITRUM_USDC_e,
            'stargate_contract': Contracts.ARBITRUM_STARGATE,
            'stargate_chain_id': 110,
            'src_pool_id': 1,
            'dst_pool_id': 1,
        },
        Networks.Avalanche.name: {
            'usdc_contract': Contracts.AVALANCHE_USDC,
            'stargate_contract': Contracts.AVALANCHE_STARGATE,
            'stargate_chain_id': 106,
            'src_pool_id': 1,
            'dst_pool_id': 1,
        },
        Networks.Polygon.name: {
            'usdc_contract': Contracts.POLYGON_USDC,
            'stargate_contract': Contracts.POLYGON_STARGATE,
            'stargate_chain_id': 109,
            'src_pool_id': 1,
            'dst_pool_id': 1,
        },
        Networks.Optimism.name: {
            'usdc_contract': Contracts.OPTIMISM_USDC_e,
            'stargate_contract': Contracts.OPTIMISM_STARGATE,
            'stargate_chain_id': 111,
            'src_pool_id': 1,
            'dst_pool_id': 1,
        },
    }

    async def send_usdc(
            self,
            to_network: Network,
            amount: Optional[TokenAmount] = None,
            slippage: float = 0.5,
            max_fee: float = 1
    ):
        failed_text = f'Faile to send {self.client.network.name} USDC to {to_network.name} USDC via Stargate'



        if self.client.network == to_network.name:
            return  f'{failed_text}: The same source network and destination networ'

        usdc_contract = await self.client.contracts.default_token(
            contract_address=Stargate.contract_data[self.client.network.name]['usdc_contract'].address)
        stargate_contract = await self.client.contracts.get(
            contract_address=Stargate.contract_data[self.client.network.name]['stargate_contract'])

        if not amount:
            amount = await self.client.wallet.balance(token=usdc_contract.address)


        lz_tx_params = TxArgs(
            dstGasForCall=0,
            dstNativeAmount=0,
            dstNativeAddr='0x0000000000000000000000000000000000000001'
        )


        args = TxArgs(
            _dstChainId=Stargate.contract_data[to_network.name]['stargate_chain_id'],
            _srcPoolId=Stargate.contract_data[to_network.name]['src_pool_id'],
            _dstPoolId=Stargate.contract_data[to_network.name]['dst_pool_id'],
            _refundAddress=self.client.account.address,
            _amountLD=amount.Wei,
            _minAmountLD=int(amount.Wei * (100 - slippage) / 100),
            _lzTxParams=lz_tx_params.tuple(),
            _to=self.client.account.address,
            _payload='0x'
        )


        value = await self.get_value(
            router_contract=stargate_contract,
            to_network=to_network,
            lz_tx_params=lz_tx_params
        )



        if not value:
            return f'{failed_text} | Can not get value ({self.client.network.name}'


        native_balance = await self.client.wallet.balance()
        if native_balance.Wei < value.Wei:
            return f'{failed_text} | Too low native balance: {native_balance.Ether}; value: {value.Ether}'

        token_price = await self.get_token_price(token_symbol=self.client.network.coin_symbol)
        network_fee = float(value.Ether) * token_price
        if network_fee > max_fee:
            return f'{failed_text} | too high fee: {network_fee} {self.client.network.name}'



        if await self.approve_interface(
            token_address=usdc_contract.address,
            spender=stargate_contract.address,
            amount=amount
        ):
            await asyncio.sleep(random.randint(5, 10))
        else:
            return f'{failed_text} | Can not approve'




        tx_params = TxParams(
            to=stargate_contract.address,
            data=stargate_contract.encodeABI('swap', args=args.tuple()),
            value=value.Wei
        )



        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)

        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return (f'{amount.Ether} USDC was send from {self.client.network.name} to {to_network.name} '
                    f'via Stargate: {tx.hash.hex()}')
        return f'{failed_text}'





    async def get_value(
            self,
            router_contract : AsyncContract,
            to_network: Network,
            lz_tx_params: TxArgs
    ) -> Optional[TokenAmount]:
        res = await router_contract.functions.quoteLayerZeroFee(
            Stargate.contract_data[to_network.name]['stargate_chain_id'],
            1,
            self.client.w3.to_bytes(text=self.client.account.address),
            self.client.w3.to_bytes(text="0x"),
            lz_tx_params.list()
        ).call()
        return TokenAmount(amount=res[0], wei=True)


    @staticmethod
    async def get_network_with_max_usdc_balance(
            address: ChecksumAddress,
    ) -> Network | None:

        supported_networks = [Networks.Arbitrum, Networks.Avalanche, Networks.Polygon, Networks.Optimism]
        max_balance = TokenAmount(amount=0)
        result_network = None
        for network in supported_networks:
            client = Client(network=network)
            balance = await client.wallet.balance(
                token=Stargate.contract_data[network.name]['usdc_contract'], address=address)
            if balance.Ether > max_balance.Ether:
                max_balance = balance
                result_network = network
        return result_network





























