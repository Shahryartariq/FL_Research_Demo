// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract FedContract {
    uint256 public globalVariable = 0;

    event GlobalVariableUpdated(uint256 newValue);
    event Print(string message);

    function setGlobalVariable(uint256 newValue) public {
        // Add the new value to the global variable and divide by 2
        globalVariable = (globalVariable + newValue) / 2;

        emit GlobalVariableUpdated(globalVariable);
    }

    function getGlobalVariable() public view returns (uint256) {
        return globalVariable;
    }

    function printHelloWorldShery() public {
        string memory hello = "Hello World Shery";
        emit Print(hello);
    }
}
