pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

import {IVRFProvider} from "../../interfaces/vrf/IVRFProvider.sol";
import {VRFConsumerBase} from "../vrf/VRFConsumerBase.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

interface INFT {
    function mint(address to, string calldata tokenURI) external;
}

abstract contract ItemMinterBase is VRFConsumerBase, Ownable {
    struct BuyOrder {
        uint256 id;
        address buyer;
        string seed;
        uint64 time;
        uint256 bounty;
        bytes32 result;
    }

    struct Item {
        uint256 id;
        string tokenURI;
    }

    // Set by the owner
    INFT public token;
    uint256 public minimumBounty = 0;
    uint256 public itemCount = 0;
    mapping(uint256 => Item) public items;

    // Set by user
    uint256 public buyOrderCount = 0;
    mapping(uint256 => BuyOrder) public buyOrders;
    mapping(string => uint256) public buyOrderKeyToBuyOrderNumber;

    event AddNewItem(uint256 id, string tokenURI);
    event EditItem(uint256 id, string tokenURI);
    event BuyRandomItem(
        uint256 id,
        address buyer,
        string seed,
        uint64 time,
        uint256 bounty
    );
    event ResolveBuyOrder(uint256 id, string seed, uint64 time, bytes32 result);

    function b32ToHexString(bytes32 x) public pure returns (string memory) {
        bytes memory s = new bytes(64);
        for (uint256 i = 0; i < 32; i++) {
            uint8 j = ((uint8(x[i]) & 240) >> 4) + 48;
            uint8 k = (uint8(x[i]) & 15) + 48;
            if (j > 57) {
                j += 39;
            }
            if (k > 57) {
                k += 39;
            }
            s[(i << 1)] = bytes1(j);
            s[(i << 1) + 1] = bytes1(k);
        }
        return string(s);
    }

    function getCurrentTimestamp() public view virtual returns (uint64) {
        return uint64(block.timestamp);
    }

    function getSeed(
        string memory prevSeed,
        uint256 _buyOrderCount,
        address buyer,
        uint64 time,
        uint256 bounty
    ) public pure returns (string memory) {
        return
            b32ToHexString(
                keccak256(
                    abi.encode(prevSeed, _buyOrderCount, buyer, time, bounty)
                )
            );
    }

    function isBuyOrderExisted(string memory seed) public view returns (bool) {
        return buyOrderKeyToBuyOrderNumber[seed] != 0;
    }

    function getBuyOrderFromSeed(string memory seed)
        public
        view
        returns (BuyOrder memory)
    {
        require(isBuyOrderExisted(seed), "ERROR_LOTTERY_NOT_FOUND");
        return buyOrders[buyOrderKeyToBuyOrderNumber[seed]];
    }

    function setMinimumBounty(uint256 newMinimumBounty) external onlyOwner {
        minimumBounty = newMinimumBounty;
    }

    function setTokenRef(INFT _token) external onlyOwner {
        token = _token;
    }

    function addItem(string calldata tokenURI) external onlyOwner {
        require(
            bytes(tokenURI).length > 0,
            "ERROR_URI_CAN_NOT_BE_EMPTY_STRING"
        );

        Item storage item = items[itemCount];

        item.id = itemCount;
        item.tokenURI = tokenURI;

        itemCount++;
        emit AddNewItem(itemCount, tokenURI);
    }

    function editItemURIAtID(uint256 id, string calldata newTokenURI)
        external
        onlyOwner
    {
        require(
            bytes(newTokenURI).length > 0,
            "ERROR_URI_CAN_NOT_BE_EMPTY_STRING"
        );
        require(id < itemCount, "ERROR_ID_OUT_OF_RANGE");

        Item storage item = items[id];
        item.tokenURI = newTokenURI;
        emit EditItem(id, newTokenURI);
    }

    function buyRandomItem() external payable {
        require(itemCount > 0, "ERROR_NOTHING_TO_BUY");

        string memory prevSeed = buyOrders[buyOrderCount].seed;
        uint256 nextBuyOrderCount = buyOrderCount + 1;
        address buyer = msg.sender;
        uint64 time = getCurrentTimestamp();
        uint256 bounty = msg.value;
        string memory seed = getSeed(
            prevSeed,
            nextBuyOrderCount,
            buyer,
            time,
            bounty
        );

        require(bounty >= minimumBounty, "ERROR_BOUNTY_TOO_LOW");

        // Request random data from the provider
        provider.requestRandomData{value: bounty}(seed, time);

        // Set mapping from seed to id/index
        buyOrderKeyToBuyOrderNumber[seed] = nextBuyOrderCount;

        // Set the value of mapping at id/index
        BuyOrder storage buyOrder = buyOrders[nextBuyOrderCount];
        buyOrder.id = nextBuyOrderCount;
        buyOrder.buyer = buyer;
        buyOrder.seed = seed;
        buyOrder.time = time;
        buyOrder.bounty = bounty;

        emit BuyRandomItem(nextBuyOrderCount, buyer, seed, time, bounty);
        // Increase buyOrderCount
        buyOrderCount = nextBuyOrderCount;
    }

    function _consume(
        string calldata seed,
        uint64 time,
        bytes32 result
    ) internal override {
        BuyOrder memory buyOrder = getBuyOrderFromSeed(seed);
        require(result != bytes32(0), "ERROR_RESULT_CAN_NOT_BE_ZERO_BYTES");
        require(
            buyOrder.result == bytes32(0),
            "ERROR_LOTTERY_ALREADY_RESOLVED"
        );
        require(buyOrder.time <= now, "ERROR_INVALID_TIMESTAMP");

        buyOrder.result = result;
        buyOrders[buyOrderKeyToBuyOrderNumber[seed]] = buyOrder;

        Item memory rewardItem = items[uint256(result) % itemCount];
        token.mint(buyOrder.buyer, rewardItem.tokenURI);

        emit ResolveBuyOrder(buyOrder.id, seed, time, result);
    }
}
