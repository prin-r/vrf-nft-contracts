from brownie.network import account
from brownie import reverts, accounts, NFT, MockItemMinter


def init_nft():
    return accounts[0].deploy(NFT, accounts[0])


def test_nft_basic_setting():
    token = init_nft()
    assert token.name() == "NFT_ITEM"
    assert token.symbol() == "ITEM"
    assert token.hasRole(token.MINTER_ROLE(), accounts[0])
    assert token.hasRole(token.DEFAULT_ADMIN_ROLE(), accounts[0])


def test_nft_minting():
    token = init_nft()

    assert token.balanceOf(accounts[0]) == 0
    assert token.totalSupply() == 0
    with reverts("ERC721Metadata: URI query for nonexistent token"):
        token.tokenURI(0)
    with reverts("ERC721: owner query for nonexistent token"):
        token.ownerOf(0)

    token.mint(accounts[0], "URI_A", {"from": accounts[0]})

    assert token.balanceOf(accounts[0]) == 1
    assert token.totalSupply() == 1
    assert token.tokenURI(0) == "URI_A"
    assert token.ownerOf(0) == accounts[0]


def test_nft_minting_fail():
    token = init_nft()

    # before
    assert token.balanceOf(accounts[0]) == 0
    assert token.totalSupply() == 0
    with reverts("ERC721Metadata: URI query for nonexistent token"):
        token.tokenURI(0)
    with reverts("ERC721: owner query for nonexistent token"):
        token.ownerOf(0)

    with reverts("Caller is not a minter"):
        token.mint(accounts[0], "URI_A", {"from": accounts[1]})

    # after
    assert token.balanceOf(accounts[0]) == 0
    assert token.totalSupply() == 0
    with reverts("ERC721Metadata: URI query for nonexistent token"):
        token.tokenURI(0)
    with reverts("ERC721: owner query for nonexistent token"):
        token.ownerOf(0)
