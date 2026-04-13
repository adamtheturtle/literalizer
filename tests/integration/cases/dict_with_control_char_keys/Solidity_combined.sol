// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;

contract Generated {
    function run() internal pure {
bytes memory my_data = abi.encode({
    "key\nwith\nnewlines": "value1",
    "key\twith\ttabs": "value2",
    "": "value3"
});
my_data = abi.encode({
    "key\nwith\nnewlines": "value1",
    "key\twith\ttabs": "value2",
    "": "value3"
});
    }
}
