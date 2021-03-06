// SPDX-License-Identifier: Apache-2.0

pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";
import {
    StdReferenceBase
} from "../../interfaces/stdreference/IStdReference.sol";

/// @title BandChain StdReferenceBasic
/// @author Band Protocol Team
contract StdReferenceBasic is AccessControl, StdReferenceBase {
    event RefDataUpdate(
        string symbol,
        uint64 rate,
        uint64 resolveTime,
        uint64 requestID
    );

    struct RefData {
        uint64 rate; // USD-rate, multiplied by 1e9.
        uint64 resolveTime; // UNIX epoch when data is last resolved.
        uint64 requestID; // BandChain request identifier for this data.
    }

    /// Mapping from token symbol to ref data
    mapping(string => RefData) public refs;

    bytes32 public constant RELAYER_ROLE = keccak256("RELAYER_ROLE");

    constructor() public {
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _setupRole(RELAYER_ROLE, msg.sender);
    }

    /// @notice Relay and save a set of price data to the contract
    /// @dev All of the lists must be of equal length
    /// @param symbols A list of symbols whose data is being relayed in this function call
    /// @param rates A list of the rates associated with each symbol
    /// @param resolveTimes A list of timestamps of when the rate data was retrieved
    /// @param requestIDs A list of BandChain request IDs in which the rate data was retrieved
    function relay(
        string[] memory symbols,
        uint64[] memory rates,
        uint64[] memory resolveTimes,
        uint64[] memory requestIDs
    ) external {
        require(hasRole(RELAYER_ROLE, msg.sender), "NOTARELAYER");
        uint256 len = symbols.length;
        require(rates.length == len, "BADRATESLENGTH");
        require(resolveTimes.length == len, "BADRESOLVETIMESLENGTH");
        require(requestIDs.length == len, "BADREQUESTIDSLENGTH");
        for (uint256 idx = 0; idx < len; idx++) {
            refs[symbols[idx]] = RefData({
                rate: rates[idx],
                resolveTime: resolveTimes[idx],
                requestID: requestIDs[idx]
            });
            emit RefDataUpdate(
                symbols[idx],
                rates[idx],
                resolveTimes[idx],
                requestIDs[idx]
            );
        }
    }

    /// @notice Returns the price data for the given base/quote pair. Revert if not available.
    /// @param base the base symbol of the token pair to query
    /// @param quote the quote symbol of the token pair to query
    function getReferenceData(string memory base, string memory quote)
        public
        view
        override
        returns (ReferenceData memory)
    {
        (uint256 baseRate, uint256 baseLastUpdate) = _getRefData(base);
        (uint256 quoteRate, uint256 quoteLastUpdate) = _getRefData(quote);
        return
            ReferenceData({
                rate: (baseRate * 1e18) / quoteRate,
                lastUpdatedBase: baseLastUpdate,
                lastUpdatedQuote: quoteLastUpdate
            });
    }

    /// @notice Get the price data of a token
    /// @param symbol the symbol of the token whose price to query
    function _getRefData(string memory symbol)
        internal
        view
        returns (uint256 rate, uint256 lastUpdate)
    {
        if (keccak256(bytes(symbol)) == keccak256(bytes("USD"))) {
            return (1e9, block.timestamp);
        }
        RefData storage refData = refs[symbol];
        require(refData.resolveTime > 0, "REFDATANOTAVAILABLE");
        return (uint256(refData.rate), uint256(refData.resolveTime));
    }
}
