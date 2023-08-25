const RatingsAndComposition = artifacts.require("RatingsAndComposition");

module.exports = function (deployer) {
    // deploy a contract
    deployer.deploy(RatingsAndComposition);
};