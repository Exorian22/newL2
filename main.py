import asyncio
import os
import time

from eth_async.client import Client
from eth_async.models import Networks, TokenAmount
from eth_async.wallet import Wallet

from data.config import pk
from data.models import Contracts
from tasks.spacefi import SpaceFi
from tasks.stargate import Stargate
from tasks.woofi import WooFi
from tasks.coredao import CoreDao
from tasks.base import Base
from tasks.uniswap import Uniswap
from tasks.syncswap import SyncSwap
from tasks.maverick import Maverick
from tasks.zksync_bridge import ZkSyncBridge
from tasks.story import Story
from tasks.syncswap_pools import SyncSwapPools

async def main():



    client = Client(private_key=pk, network=Networks.ZkSync)
    spacefi = SpaceFi(client=client)
    stargate = Stargate(client=client)
    woofi = WooFi(client=client)
    coredao = CoreDao(client=client)
    base = Base(client=client)
    uniswap = Uniswap(client=client)
    syncswa = SyncSwap(client=client)
    maverick = Maverick(client=client)
    zksyncbridge = ZkSyncBridge(client=client)
    story = Story(client=client)
    syncswap_pools = SyncSwapPools(client=client)



    eth_amount = TokenAmount(amount=0.2)
    #
    # input_data = '0xad271fa300000000000000000000000045856bd6bb9f076f4c558a4d5932c6c8d832b0d00000000000000000000000000000000000000000000000000001f77f68c439ea00000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000120000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001800000000000000000000000000000000000000000000000000000000000000040000000000000000000000000f9abf2a96174e8a1f35900167463298476dc58a20000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000001610cac694e97e0000000000000000000000000000000000000000000000000000003c8c2ecc16b0000000000000000000000000000000000000000000000000000000000000000'
    # base.parse_params_me(params=input_data)

    # res = await spacefi.swap_eth_to_usdt(amount=eth_amount)

    # res = await syncswap_pools.add_liqudity_to_zk_eth_pool(eth_amount)
    #
    #
    # print(res)

    # balance = await client.wallet.balance(token='0x45856bD6Bb9f076F4C558A4D5932c6c8d832b0d0')
    # print(balance)

    # def get_contract(self, contract_address: str, abi: dict = ERC20_ABI) -> AsyncContract:
    #     return self.w3.eth.contract(
    #         address=web3.to_checksum_address(contract_address),
    #         abi=abi
    #     )
    #
    # res = await syncswap_pools.add_liquidity_zk_eth(first_token_amount=0.1)
    # print(res)

    # mem = await syncswap_pools.withdraw_liquidity(first_token=Contracts.ZKSYNC_ZK, second_token=Contracts.ZKSYNC_ETH)
    # print(mem)


    # res = await story.mint_nft()
    # print(res)
    #
    # i += 1
    # time.sleep(30)

    print(awai)


if __name__ == '__main__':
    asyncio.run(main())