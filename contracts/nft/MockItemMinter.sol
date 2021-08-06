pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

import {IVRFProvider} from "../../interfaces/vrf/IVRFProvider.sol";
import {ItemMinterBase} from "./ItemMinterBase.sol";

contract MockItemMinter is ItemMinterBase {
    uint64 public timestamp = 0;

    constructor(IVRFProvider _provider, uint256 _minimumBounty) public {
        provider = _provider;
        minimumBounty = _minimumBounty;
    }

    function setProvider(IVRFProvider newProvider) public onlyOwner {
        provider = newProvider;
    }

    function setTimestamp(uint64 newTimestamp) public onlyOwner {
        timestamp = newTimestamp;
    }

    function getCurrentTimestamp() public view override returns (uint64) {
        return timestamp;
    }
}
