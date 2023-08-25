// JavaScript source code
const Migrations = artifacts.require("Migrations");

module.exports = function (deployer) {
    deployer.deploy(Migrations);
};