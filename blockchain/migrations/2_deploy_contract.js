var AccessLog = artifacts.require('./AccessLog');

module.exports = function(deployer) {
    deployer.deploy(AccessLog);
}
