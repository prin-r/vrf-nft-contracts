from brownie.network import account
import brownie
from brownie import Wei, accounts, NFT, MockItemMinter, MockBridgeForVRF
from contest import vrf_provider, proof_1


def init_nft():
    return accounts[0].deploy(NFT, accounts[0])


def init_mock_minter_and_vp():
    vp = vrf_provider()
    mock_minter = accounts[0].deploy(MockItemMinter, vp.address, Wei("0.12 ether"))
    token = accounts[0].deploy(NFT, mock_minter.address)
    mock_minter.setTokenRef(token.address, {"from": accounts[0]})
    mock_minter.addItem("ITEM_A", {"from": accounts[0]})
    mock_minter.addItem("ITEM_B", {"from": accounts[0]})
    mock_minter.addItem("ITEM_C", {"from": accounts[0]})

    assert mock_minter.items(0) == (0, "ITEM_A")
    assert mock_minter.items(1) == (1, "ITEM_B")
    assert mock_minter.items(2) == (2, "ITEM_C")

    return vp, mock_minter, token


def test_nft_and_minter_1():
    vp, mock_minter, token = init_mock_minter_and_vp()
    test_time = 1608162982
    test_bounty = Wei("0.15 ether")
    test_buyer = accounts[1]

    assert token.balanceOf(test_buyer) == 0
    assert token.totalSupply() == 0

    mock_minter.setTimestamp(test_time, {"from": accounts[0]})

    assert mock_minter.buyOrders(0) == (0, "0x" + ("00" * 20), "", 0, 0, "0x" + ("00" * 32))
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

    assert token.balanceOf(test_buyer) == 0
    assert token.totalSupply() == 0

    bounty_hunter = accounts[2]
    bounty_hunter_prev_balance = bounty_hunter.balance()
    tx = vp.relayProof(mock_minter.address, bytes.fromhex(proof_1), {"from": bounty_hunter})
    assert tx.status == 1

    assert bounty_hunter.balance() == bounty_hunter_prev_balance + test_bounty
    assert token.balanceOf(test_buyer) == 1
    assert token.totalSupply() == 1
    # assert mock_minter.buyOrders(0) == (0, "0x" + ("00" * 20), "", 0, 0, "0x" + ("00" * 32))
    assert mock_minter.buyOrderCount() == 1
