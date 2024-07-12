// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Laplace {
    uint256 private sensitivity;
    uint256 private epsilon;

    // Initialize sensitivity and privacy budget (epsilon)
    constructor(uint256 _sensitivity, uint256 _epsilon) {
        sensitivity = _sensitivity;
        epsilon = _epsilon;
    }

    // Function to add Laplace noise
    function addNoise(uint256 value) public view returns (uint256) {
        // Sample from Laplace distribution
        uint256 noise = laplaceNoise();

        // Clip the noise
        if (noise > sensitivity * epsilon) {
            noise = sensitivity * epsilon;
        }

        // Add the noise to the value
        return value + noise;
    }

    // Sample from a Laplace distribution
    function laplaceNoise() internal view returns (uint256) {
        // Generate random number using block randomness
        uint256 seed = uint256(keccak256(abi.encodePacked(blockhash(block.number - 1))));
        uint256 randomNumber = uint256(keccak256(abi.encodePacked(seed)));

        // Convert the random number to a Laplace noise
        // You can use a library or custom implementation for Laplace noise generation
        // For simplicity, let's use a basic implementation here
        uint256 noise = uint256(keccak256(abi.encodePacked(randomNumber))) % (2 * sensitivity * epsilon);

        return noise;
    }
}
