pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract NFT is ERC721, AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    constructor(address minter) public ERC721("NFT_ITEM", "ITEM") {
        _setupRole(MINTER_ROLE, minter);
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    function mint(address to, string calldata tokenURI) external {
        require(hasRole(MINTER_ROLE, msg.sender), "Caller is not a minter");

        uint256 newItemId = totalSupply();
        _safeMint(to, newItemId);
        _setTokenURI(newItemId, tokenURI);
    }
}
