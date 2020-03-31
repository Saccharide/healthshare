var Web3 = require("web3");
var Web3 = require('web3');

var provider = new Web3.providers.HttpProvider("http://localhost:9545");
var web3 = new Web3(provider);
var contract = require("@truffle/contract");

var AccessLog = contract(require("./build/contracts/AccessLog.json"))

const express = require('express')
var bodyParser = require('body-parser')

const app = express()
app.use(bodyParser.json())
var instance = null;
var accounts = null;


async function main() {
  accounts = await web3.eth.getAccounts();
  AccessLog.setProvider(provider);
  instance = await AccessLog.deployed();
  console.log("Server listening on port 3000");
  app.listen(3000)
}

app.get('/getPublicKey', async function (req, res) {
  res.json({
    data: await instance.getPublicKey.call({from: req.body.user_id})
  });
})

app.post('/setPublicKey', async function (req, res) {
  res.json({
    data: await instance.setPublicKey.sendTransaction(req.body.public_key, {from: req.body.user_id})
  });
})

main()

// AccessLog.deployed().then((instance)=>{
//   return instance.setPublicKey(
//     "MEH",
//     {from: "0xDE6bC281B6D3844C60A38E6F5Ed1eE8729929492"}
//   );
// }).then(() => {
//   return accessLog.getPublicKey();
// }).then( (result) => {
//   console.log(result);
// });

// AccessLog.deployed().then(function(instance) {
//   deployed = instance;
//   return instance.someFunction(5);
// }).then(function(result) {
//   // Do something with the result or continue with more transactions.
// });
