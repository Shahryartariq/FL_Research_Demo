// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract myTime {
    uint256 public lastGasUsed;

    function measureLoopGas() public {
        uint256 gasBefore = gasleft();
        for (uint256 i = 0; i < 100; i++) {
            uint256 x = i;
        }
        uint256 gasAfter = gasleft();
        lastGasUsed = gasBefore - gasAfter;
    }
}
