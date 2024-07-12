const FedContract = artifacts.require("FedContract");

module.exports = function (deployer) {
  deployer.deploy(FedContract);
};
