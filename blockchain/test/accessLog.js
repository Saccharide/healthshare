const AccessLog = artifacts.require('AccessLog');

contract('AccessLog', () => {
    it('Should deploy smart contract properly', async () => {
        // Waiting till a depolyed javascript object of a smart contract is deployed
        const accessLog = await AccessLog.deployed();
        // Now able to interact with the smart contract, and call all its functions.
        console.log(accessLog.address);
        assert(accessLog.address !== '');
    });
});
