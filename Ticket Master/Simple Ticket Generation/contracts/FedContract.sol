// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract FedContract {
    address public serverAddress = 0xbF490187D9c9F66496bC400C50F37e61Fc336A8f;
    address[] private clientAddresses;

    uint256 private counter;

    modifier onlyServerAndClients() {
        require(msg.sender == serverAddress || isClient(msg.sender), "Only server and clients can call this function");
        _;
    }

    modifier onlyServer() {
        require(msg.sender == serverAddress, "Only server can call this function");
        _;
    }

    constructor() {
        clientAddresses.push(0x96692F3D2a0222072B990174eD8F0193690E4270);
        clientAddresses.push(0xD71719FF94B3F1f306dF5af3B3E38EC6d32c955b);
        clientAddresses.push(0xe5B5B58dBACcA0c6ad3cAE5785b63C822553B5Fb);
    }

    function isClient(address _address) private view returns (bool) {
        for (uint256 i = 0; i < clientAddresses.length; i++) {
            if (clientAddresses[i] == _address) {
                return true;
            }
        }
        return false;
    }

    function getClientAddresses() external view returns (address[] memory) {
        return clientAddresses;
    }

    function setVariable(uint256 _value) external onlyServerAndClients {
        counter = (counter + _value) / 2;
    }

    function getVariable() external view onlyServer returns (uint256) {
        return counter;
    }

    function helloWorld() external pure returns (string memory) {
        return "Hello World!";
    }
}

 
