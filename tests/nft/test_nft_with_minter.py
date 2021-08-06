from brownie.network import account
import brownie
from brownie import Wei, accounts, NFT, MockItemMinter, MockBridgeForVRF
from contest import vrf_provider, proof_1

ITEMS = [(0, "ITEM_A"), (1, "ITEM_B"), (2, "ITEM_C"), (3, "ITEM_D"), (4, "ITEM_E")]


def init_nft():
    return accounts[0].deploy(NFT, accounts[0])


def init_mock_minter_and_vp():
    vp = vrf_provider()
    mock_minter = accounts[0].deploy(MockItemMinter, vp.address, Wei("0.12 ether"))
    token = accounts[0].deploy(NFT, mock_minter.address)
    mock_minter.setTokenRef(token.address, {"from": accounts[0]})

    for i in range(len(ITEMS)):
        mock_minter.addItem(ITEMS[i][1], {"from": accounts[0]})
        assert mock_minter.items(i) == ITEMS[i]

    assert mock_minter.itemCount() == len(ITEMS)

    return vp, mock_minter, token


def test_nft_and_minter_1():
    vp, mock_minter, token = init_mock_minter_and_vp()
    test_time = 1608162982
    test_bounty = Wei("0.15 ether")
    test_buyer = accounts[1]

    assert token.balanceOf(test_buyer) == 0
    assert token.totalSupply() == 0

    mock_minter.setTimestamp(test_time, {"from": accounts[0]})

    assert mock_minter.buyOrders(1) == (0, "0x" + ("00" * 20), "", 0, 0, "0x" + ("00" * 32))
    assert mock_minter.buyOrderCount() == 0

    test_seed = mock_minter.getSeed("", 1, test_buyer, test_time, test_bounty)
    mock_minter.buyRandomItem({"from": test_buyer, "value": test_bounty})

    assert mock_minter.buyOrders(1) == (
        1,
        test_buyer,
        test_seed,
        test_time,
        test_bounty,
        "0x" + ("00" * 32),
    )
    assert mock_minter.buyOrderCount() == 1

    assert mock_minter.buyOrders(1) == (
        1,
        test_buyer,
        test_seed,
        test_time,
        test_bounty,
        "0x" + ("00" * 32),
    )
    assert mock_minter.buyOrderCount() == 1

    assert token.balanceOf(test_buyer) == 0
    assert token.totalSupply() == 0

    bounty_hunter = accounts[2]
    bounty_hunter_prev_balance = bounty_hunter.balance()
    tx = vp.relayProof(mock_minter.address, bytes.fromhex(proof_1), {"from": bounty_hunter})
    assert tx.status == 1

    expected_result = "0x236a56134f886fe84f50d12b0e9d248f2f3ffa9ce5a4980c2c2084a0a9585fd7"
    assert bounty_hunter.balance() == bounty_hunter_prev_balance + test_bounty
    assert mock_minter.buyOrders(1) == (
        1,
        test_buyer,
        test_seed,
        test_time,
        test_bounty,
        expected_result,
    )
    assert mock_minter.buyOrderCount() == 1

    assert token.balanceOf(test_buyer) == 1
    assert token.totalSupply() == 1
    assert token.ownerOf(0) == test_buyer
    assert token.tokenURI(0) == ITEMS[int(expected_result, 16) % len(ITEMS)][1]
