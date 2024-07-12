const myTime = artifacts.require("myTime");

module.exports = function(deployer) {
  deployer.deploy(myTime);
};