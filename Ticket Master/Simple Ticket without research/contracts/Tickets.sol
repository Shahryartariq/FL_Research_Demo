// SPDX-License-Identifier: MIT 
pragma solidity >=0.4.22 <0.9.0;

uint256 constant TOTAL_TICKETS = 10;

contract Tickets {
  address public owner = msg.sender;

  struct Ticket {
    uint256 price;
    address owner;
  }

  Ticket[TOTAL_TICKETS] public tickets;

  constructor() {
    for (uint256 i = 0; i < TOTAL_TICKETS; i++) {
      tickets[i].price = 1e17; // 0.1 ETH
      tickets[i].owner = address(0x0);
    }
  }

  function buyTicket(uint256 _index) external payable {
    require(_index < TOTAL_TICKETS && _index >= 0);
    require(tickets[_index].owner == address(0x0));
    require(msg.value >= tickets[_index].price);
    tickets[_index].owner = msg.sender;
  }
}


contract federated_learning {
  /* Define variables and their types */
  string ModelWeights;
  uint256 totalSubmissions = 0;
  uint256 totalWeight = 0;
  bytes32 clientMerkleRoot;

  struct Entity {
    string publicKey;
    uint256 weight;
  }

  mapping(address => Entity) clients;
  Entity server;

  /* Constructor */
  FUNCTION constructor(bytes32 _clientMerkleRoot) {
    Initialize ModelWeights;
    server = Entity("server_public_key", 0);
    clientMerkleRoot = _clientMerkleRoot;
    totalSubmissions = 0;
    totalWeight = 0;
  }


/* Function to submit weight */
  FUNCTION submitWeight(uint256 newWeight, bytes32[] merkleProof) {
    IF verifyClient(msg.sender, merkleProof) == true THEN
      clients[msg.sender].weight = newWeight;
      totalWeight += newWeight;
      totalSubmissions += 1;
    ENDIF
  }
  
  /* Function to apply federated averaging */
  FUNCTION applyFederatedAveraging() onlyOwner {
    IF totalSubmissions > 0 THEN
      uint256 federatedAverage = totalWeight / totalSubmissions;
      federatedAverage += generateLaplaceNoise();
      server.weight = federatedAverage;
      totalWeight = 0;
      totalSubmissions = 0;
    ENDIF
  }


