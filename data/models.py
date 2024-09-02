from eth_async.models import RawContract, DefaultABIs
from eth_async.utils.utils import read_json
from eth_async.classes import Singleton

from data.config import ABIS_DIR

class Contracts(Singleton):
    # Arbitrum
    ARBITRUM_WOOFI = RawContract(
        title="WooFi",
        address='0x9aed3a8896a85fe9a8cac52c9b402d092b629a30',
        abi=read_json(path=(ABIS_DIR, 'woofi.json'))
    )

    ARBITRUM_USDC = RawContract(
        title='USDC',
        address='0xaf88d065e77c8cC2239327C5EDb3A432268e5831',
        abi=DefaultABIs.Token
    )

    ARBITRUM_ETH = RawContract(
        title='ETH',
        address='0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
        abi=DefaultABIs.Token
    )

    ARBITRUM_USDC_e = RawContract(
        title='USDC',
        address='0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8',
        abi=DefaultABIs.Token
    )

    ARBITRUM_GETH = RawContract(
        title='GETH',
        address='0xdD69DB25F6D620A7baD3023c5d32761D353D3De9',
        abi=DefaultABIs.Token
    )

    ARBITRUM_STARGATE = RawContract(
        title='arbitrum_stargate',
        address='0x53Bf833A5d6c4ddA888F69c22C88C9f356a41614',
        abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    ARBITRUM_UNISWAP = RawContract(
        title='arbitrum_uniswap',
        address='0x5E325eDA8064b456f4781070C0738d849c824258',
        abi=read_json(path=(ABIS_DIR, 'uniswap.json'))
    )

    ARBITRUM_CAMELOT = RawContract(
        title='arbitrum_camelot',
        address='0x99D4e80DB0C023EFF8D25d8155E0dCFb5aDDeC5E',
        abi=read_json(path=(ABIS_DIR, 'camelot.json'))
    )

    ARBITRUM_ARB = RawContract(
        title='ARB',
        address='0x912CE59144191C1204E64559FE8253a0e49E6548',
        abi=DefaultABIs.Token
    )

    # ETHEREUM
    ETHEREUM_SHIBA = RawContract(
        title="Shiba",
        address='0x03f7724180AA6b939894B5Ca4314783B0b36b329',
        abi=read_json(path=(ABIS_DIR, 'shiba.json'))
    )

    ETHEREUM_USDC = RawContract(
        title="USDC",
        address='0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
        abi=DefaultABIs.Token
    )

    ETHEREUM_ETH = RawContract(
        title="ETH",
        address="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        abi=DefaultABIs.Token
    )

    #ZKSYNC
    ZKSYNC_SPACEFI = RawContract(
        title='SpaceFi',
        address='0xbE7D1FD1f6748bbDefC4fbaCafBb11C6Fc506d1d',
        abi=read_json(path=(ABIS_DIR, 'spacefi.json'))
    )

    ZKSYNC_UNISWAP = RawContract(
        title='zksync_uniswap',
        address='0x28731BCC616B5f51dD52CF2e4dF0E78dD1136C06',
        abi=read_json(path=(ABIS_DIR, 'uniswap.json'))
    )

    ZKSYNC_ETH = RawContract(
        title="ETH",
        address="0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
        abi=DefaultABIs.Token
    )

    ZKSYNC_WBTC = RawContract(
        title="WBTC",
        address="0xBBeB516fb02a01611cBBE0453Fe3c580D7281011",
        abi=DefaultABIs.Token
    )

    ZKSYNC_USDT = RawContract(
        title="USDT",
        address="0x493257fD37EDB34451f62EDf8D2a0C418852bA4C",
        abi=DefaultABIs.Token
    )

    ZKSYNC_USDC = RawContract(
        title="USDC",
        address="0x1d17CBcF0D6D143135aE902365D2E5e2A16538D4",
        abi=DefaultABIs.Token
    )

    ZKSYNC_USDC_E = RawContract(
        title="USDC_E",
        address="0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4",
        abi=DefaultABIs.Token
    )

    ZKSYNC_SYNCSWAP = RawContract(
        title="zksync_syncswap",
        address="0x2da10A1e27bF85cEdD8FFb1AbBe97e53391C0295",
        abi=read_json(path=(ABIS_DIR, 'syncswap.json'))
    )

    ZKSYNC_SYNCSWAP_POOL = RawContract(
        title="zksync_syncswap_pool",
        address="0xf2DAd89f2788a8CD54625C60b55cD3d2D0ACa7Cb",
        abi=read_json(path=(ABIS_DIR, 'test_syncswap.json'))
    )

    ZK_SYNCSWAP_ROUTER_V2 = RawContract(
        title='zksync_router_v2',
        address='0x9B5def958d0f3b6955cBEa4D5B7809b2fb26b059',
        abi=read_json(path=(ABIS_DIR, 'syncswap_router_v2.json'))
    )

    ZKSYNC_ZK = RawContract(
        title="ZK",
        address="0x5A7d6b2F92C77FAD6CCaBd7EE0624E64907Eaf3E",
        abi=DefaultABIs.Token
    )

     # SyncSwap pool addresses
    SYNCSWAP_ETH_USDC_POOL = RawContract(
        address='0x80115c708E12eDd42E504c1cD52Aea96C547c05c'
    )
    SYNCSWAP_ETH_USDT_POOL = RawContract(
        address='0xd3D91634Cf4C04aD1B76cE2c06F7385A897F54D3'
    )
    SYNCSWAP_ETH_BUSD_POOL = RawContract(
        address='0xad86486f1d225d624443e5df4b2301d03bbe70f6'
    )
    SYNCSWAP_ETH_WBTC_POOL = RawContract(
        address='0xb3479139e07568ba954c8a14d5a8b3466e35533d'
    )

    SYNCSWAP_ETH_ZK_POOL = RawContract(
        address='0x45856bd6bb9f076f4c558a4d5932c6c8d832b0d0'
    )

    MAVERICK_ETH_USDCE_CONTRACT = RawContract(
        address='0x621c665730ee87e1425dbdd3a2de54ad29fc9de0',
        abi=read_json(path=(ABIS_DIR, 'maverick.json'))
    )

    BRIDGE_ETH_TO_ZKSYNC = RawContract (
        address='0x32400084C286CF3E17e7B677ea9583e60a000324',
        abi=read_json(path=(ABIS_DIR, 'bridge_to_zk.json'))
    )




    WETH = RawContract(
        title='WETH',
        address='0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91',
        abi=read_json(path=(ABIS_DIR, 'WETH.json'))
    )

    POLYGON_STARGATE = RawContract(
        title='polygon_stargate',
        address='0x45A01E4e04F14f7A4a6702c74187c5F6222033cd',
        abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    POLYGON_USDT = RawContract(
        title="USDT",
        address="0xc2132d05d31c914a87c6611c10748aeb04b58e8f",
        abi=DefaultABIs.Token
    )

    POLYGON_USDC = RawContract(
        title="USDC",
        address="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
        abi=DefaultABIs.Token
    )

    AVALANCHE_STARGATE = RawContract(
        title='avalanche_stargate',
        address='0x45A01E4e04F14f7A4a6702c74187c5F6222033cd',
        abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    AVALANCHE_USDC = RawContract(
        title="USDC",
        address="0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E",
        abi=DefaultABIs.Token
    )

    OPTIMISM_ETH = RawContract(
        title="ETH",
        address="0x4200000000000000000000000000000000000006",
        abi=DefaultABIs.Token
    )

    OPTIMISM_USDC = RawContract(
        title="USDC",
        address="0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85",
        abi=DefaultABIs.Token
    )

    OPTIMISM_USDC_e = RawContract(
        title="USDC_e",
        address="0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
        abi=DefaultABIs.Token
    )

    OPTIMISM_USDT = RawContract(
        title="USDT",
        address="0x94b008aA00579c1307B0EF2c499aD98a8ce58e58",
        abi=DefaultABIs.Token
    )
    OPTIMISM_STARGATE = RawContract(
        title="optimism_stargate",
        address="0xb0d502e938ed5f4df2e681fe6e419ff29631d62b",
        abi=read_json(path=(ABIS_DIR, 'stargate.json'))
    )

    BSC_COREDAO_BRIDGE = RawContract(
        title="bsc_stargate",
        address="0x52e75D318cFB31f9A2EdFa2DFee26B161255B233",
        abi=read_json(path=(ABIS_DIR, 'coredao.json'))
    )

    BSC_USDT = RawContract(
        title='USDT',
        address='0x55d398326f99059fF775485246999027B3197955',
        abi=DefaultABIs.Token
    )




