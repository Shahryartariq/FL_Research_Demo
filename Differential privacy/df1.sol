// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LaplaceMechanism {
    // Event to log perturbed result
    event PerturbedResult(uint256 result);

    // Function to add Laplace noise
    function laplaceMechanism(uint256 queryResult, uint256 sensitivity, uint256 epsilon) external pure returns (uint256) {
        // Calculate scale
        uint256 scale = sensitivity / epsilon;
        // Generate pseudo-random noise using blockhash
        uint256 noise = uint256(keccak256(abi.encodePacked(blockhash(block.number)))) % (2 * scale + 1) - scale;
        // Calculate perturbed result
        uint256 perturbedResult = queryResult + noise;
        // Emit event
        emit PerturbedResult(perturbedResult);
        return perturbedResult;
    }
}
