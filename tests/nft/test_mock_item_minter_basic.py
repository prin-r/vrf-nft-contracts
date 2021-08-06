from brownie.network import account
from brownie import reverts, accounts, Wei, MockItemMinter
from contest import vrf_provider


def init_mock_minter_and_vp():
    vp = vrf_provider()
    return (accounts[0].deploy(MockItemMinter, vp.address, Wei("1 finney")), vp)


def test_basic_minter_setting():
    mock_minter, vp = init_mock_minter_and_vp()

    assert mock_minter.getCurrentTimestamp() == 0
    assert mock_minter.provider() == vp.address
    assert mock_minter.minimumBounty() == Wei("1 finney")
    assert mock_minter.itemCount() == 0
    assert mock_minter.buyOrderCount() == 0
    assert mock_minter.buyOrderKeyToBuyOrderNumber("") == 0
    assert mock_minter.buyOrderKeyToBuyOrderNumber("xxx") == 0
    assert mock_minter.items(0) == (0, "")
    assert mock_minter.items(999) == (0, "")
    assert mock_minter.buyOrders(0) == (0, "0x" + ("00" * 20), "", 0, 0, "0x" + ("00" * 32))
    assert mock_minter.buyOrders(999) == (0, "0x" + ("00" * 20), "", 0, 0, "0x" + ("00" * 32))


def test_basic_getter():
    mock_minter, _ = init_mock_minter_and_vp()

    test_prev_seed = "832334ed2fcd3ddb02edc2fa372753c92bfcf23abfd03414ae2320613e9f1489"
    test_seed = "afac4401019ced0603ae2ad5ba6ff6f8b3013eea2962e8fc77c6d807d85b1f2b"
    test_buy_order_count = 0
    test_buyer = accounts[1]
    test_time = 1628162982
    test_bounty = Wei("1 finney")

    assert mock_minter.minimumBounty() == Wei("1 finney")
    assert mock_minter.itemCount() == 0
    assert mock_minter.buyOrderCount() == 0
    assert mock_minter.getCurrentTimestamp() == 0
    assert mock_minter.b32ToHexString(bytes.fromhex(test_seed)) == test_seed
    assert (
        mock_minter.getSeed(
            test_prev_seed, test_buy_order_count, test_buyer, test_time, test_bounty
        )
        == test_seed
    )
    assert mock_minter.isBuyOrderExisted(test_seed) == False
    with reverts("ERROR_LOTTERY_NOT_FOUND"):
        assert mock_minter.getBuyOrderFromSeed(test_seed)


def test_basic_setter_success():
    mock_minter, _ = init_mock_minter_and_vp()
    test_time = 1628162982
    test_new_bounty = Wei("99 szabo")

    assert mock_minter.getCurrentTimestamp() == 0
    mock_minter.setTimestamp(test_time)
    assert mock_minter.getCurrentTimestamp() == test_time

    assert mock_minter.minimumBounty() == Wei("1 finney")
    mock_minter.setMinimumBounty(test_new_bounty, {"from": accounts[0]})
    assert mock_minter.minimumBounty() == test_new_bounty

    assert mock_minter.token() == "0x" + ("00" * 20)
    mock_minter.setTokenRef(accounts[0], {"from": accounts[0]})
    assert mock_minter.token() == accounts[0]

    assert mock_minter.items(0) == (0, "")
    assert mock_minter.itemCount() == 0
    mock_minter.addItem("ITEM_A", {"from": accounts[0]})
    assert mock_minter.items(0) == (0, "ITEM_A")
    assert mock_minter.itemCount() == 1

    mock_minter.editItemURIAtID(0, "ITEM_AAA", {"from": accounts[0]})
    assert mock_minter.items(0) == (0, "ITEM_AAA")
    assert mock_minter.itemCount() == 1

    # Test buying 1
    genesis_seed = ""
    test_buyer = accounts[1]
    buy_order_count = mock_minter.buyOrderCount()
    buy_order_seed = mock_minter.getSeed(
        genesis_seed, buy_order_count + 1, test_buyer, test_time, test_new_bounty
    )

    assert mock_minter.isBuyOrderExisted(buy_order_seed) == False
    mock_minter.buyRandomItem({"from": test_buyer, "value": test_new_bounty})
    assert mock_minter.buyOrderCount() == 1
    assert mock_minter.isBuyOrderExisted(buy_order_seed) == True

    assert mock_minter.getBuyOrderFromSeed(buy_order_seed) == (
        1,
        test_buyer,
        buy_order_seed,
        test_time,
        test_new_bounty,
        "0x" + ("00" * 32),
    )
    assert mock_minter.getBuyOrderFromSeed(buy_order_seed) == mock_minter.buyOrders(1)

    # Test buying 2
    buy_order_count2 = mock_minter.buyOrderCount()
    assert buy_order_count2 == buy_order_count + 1

    buy_order_seed2 = mock_minter.getSeed(
        buy_order_seed, buy_order_count2 + 1, test_buyer, test_time, test_new_bounty
    )
    assert buy_order_seed2 != buy_order_seed

    assert mock_minter.isBuyOrderExisted(buy_order_seed2) == False
    mock_minter.buyRandomItem({"from": test_buyer, "value": test_new_bounty})
    assert mock_minter.isBuyOrderExisted(buy_order_seed2) == True

    assert mock_minter.getBuyOrderFromSeed(buy_order_seed2) == (
        2,
        test_buyer,
        buy_order_seed2,
        test_time,
        test_new_bounty,
        "0x" + ("00" * 32),
    )
    assert mock_minter.getBuyOrderFromSeed(buy_order_seed2) == mock_minter.buyOrders(2)


def test_basic_setter_fail():
    mock_minter, vp = init_mock_minter_and_vp()

    none_owner = accounts[1]

    with reverts("Ownable: caller is not the owner"):
        mock_minter.setMinimumBounty(Wei("2.5 ether"), {"from": none_owner})

    with reverts("Ownable: caller is not the owner"):
        mock_minter.setTokenRef(accounts[0], {"from": none_owner})

    with reverts("Ownable: caller is not the owner"):
        mock_minter.addItem("ITEM_A", {"from": none_owner})

    with reverts("ERROR_URI_CAN_NOT_BE_EMPTY_STRING"):
        mock_minter.addItem("", {"from": accounts[0]})

    with reverts("Ownable: caller is not the owner"):
        mock_minter.editItemURIAtID(0, "ITEM_AAA", {"from": none_owner})

    with reverts("ERROR_URI_CAN_NOT_BE_EMPTY_STRING"):
        mock_minter.editItemURIAtID(0, "", {"from": accounts[0]})

    with reverts("ERROR_ID_OUT_OF_RANGE"):
        mock_minter.editItemURIAtID(1, "ITEM_AAA", {"from": accounts[0]})

    test_new_bounty = Wei("1 finney")
    test_buyer = accounts[1]

    with reverts("ERROR_NOTHING_TO_BUY"):
        mock_minter.buyRandomItem({"from": test_buyer, "value": test_new_bounty})

    mock_minter.addItem("ITEM_A", {"from": accounts[0]})

    with reverts("ERROR_BOUNTY_TOO_LOW"):
        mock_minter.buyRandomItem({"from": test_buyer, "value": Wei("0.9 finney")})

    with reverts("Caller is not the provider"):
        test_seed = "38c6c39eb93a921f80b1ae4127f7d9c9e6e28920dad32247709ef3363d96c5f1"
        test_time = 1628162982
        test_result = "39e9c517b02ed0e5fa4200fd9474720de4f1723ba92490f28719d01d6f499882"
        mock_minter.consume(test_seed, test_time, bytes.fromhex(test_result), {"from": none_owner})

    with reverts("ERROR_LOTTERY_NOT_FOUND"):
        mock_minter.setProvider(accounts[0], {"from": accounts[0]})
        genesis_seed = ""
        test_time = 1628162982
        test_result = "39e9c517b02ed0e5fa4200fd9474720de4f1723ba92490f28719d01d6f499882"
        mock_minter.consume(
            genesis_seed, test_time, bytes.fromhex(test_result), {"from": accounts[0]}
        )

    with reverts("ERROR_RESULT_CAN_NOT_BE_ZERO_BYTES"):
        mock_minter.setProvider(vp.address, {"from": accounts[0]})
        genesis_seed = ""
        buy_order_count = 0
        test_result = "00" * 32

        test_time = 555
        mock_minter.setTimestamp(test_time)

        buy_order_seed = mock_minter.getSeed(
            genesis_seed, buy_order_count + 1, test_buyer, test_time, test_new_bounty
        )

        mock_minter.buyRandomItem({"from": test_buyer, "value": test_new_bounty})
        mock_minter.setProvider(accounts[0], {"from": accounts[0]})

        mock_minter.consume(
            buy_order_seed, test_time, bytes.fromhex(test_result), {"from": accounts[0]}
        )

    with reverts("ERROR_INVALID_TIMESTAMP"):
        mock_minter.setProvider(vp.address, {"from": accounts[0]})
        prev_seed = mock_minter.buyOrders(mock_minter.buyOrderCount())[2]
        buy_order_count = 1
        test_result = "12" * 32

        test_time = 2 ** 63
        mock_minter.setTimestamp(test_time)

        buy_order_seed = mock_minter.getSeed(
            prev_seed, buy_order_count + 1, test_buyer, test_time, test_new_bounty
        )

        mock_minter.buyRandomItem({"from": test_buyer, "value": test_new_bounty})
        mock_minter.setProvider(accounts[0], {"from": accounts[0]})

        mock_minter.consume(
            buy_order_seed, test_time, bytes.fromhex(test_result), {"from": accounts[0]}
        )
