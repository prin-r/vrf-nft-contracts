// SPDX-License-Identifier: Apache-2.0

pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

import {IBridge} from "../../interfaces/bridge/IBridge.sol";
import {Packets} from "../bridge/library/Packets.sol";

contract MockPackets {
    function encodeRequestPacket(IBridge.RequestPacket memory _packet)
        public
        pure
        returns (bytes memory)
    {
        return Packets.encodeRequestPacket(_packet);
    }

    function encodeResponsePacket(IBridge.ResponsePacket memory _packet)
        public
        pure
        returns (bytes memory)
    {
        return Packets.encodeResponsePacket(_packet);
    }

    function getEncodedResult(
        IBridge.RequestPacket memory _req,
        IBridge.ResponsePacket memory _res
    ) public pure returns (bytes memory) {
        return Packets.getEncodedResult(_req, _res);
    }
}
