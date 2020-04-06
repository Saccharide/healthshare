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

function str2array(string, delimiter) {
  if (!delimiter) {
    delimiter = "\n";
  }
  return string
    .split(delimiter)
    .filter((v, i, self) => v.length && self.indexOf(v) === i) ;
}

async function main() {
  accounts = await web3.eth.getAccounts();
  AccessLog.setProvider(provider);
  instance = await AccessLog.deployed();
  console.log("Server listening on port 3000");
  app.listen(3000)
}

app.get('/getPublicKey', async function (req, res) {
  res.json({
    data: await instance.getPublicKey.call()
  });
})

app.post('/setPublicKey', async function (req, res) {
  res.json({
    data: await instance.setPublicKey.sendTransaction(req.body.public_key, {from: req.body.user_id})
  });
})

app.post('/addFile', async function (req, res) {
  res.json({
    data: await instance.addFilename.sendTransaction(req.body.file_name, {from: req.body.user_id})
  });
})

app.get('/getFiles', async function (req, res) {
  var address = (req.query.user_id);
  res.json({
    data: str2array(await instance.getFiles.call(address))
  });
})

app.post('/setDetails', async function (req, res) {
  var address = req.body.user_id;
  res.json({
    data: await instance.setEthereumAdress.sendTransaction(
      req.body.name,
      req.body.birthday,
      {from: address}
    )
  });
})


app.get('/getAddressFromDetails', async function (req, res) {
  res.json({
    data: await instance.getEthereumAdress.call(
      req.query.name,
      req.query.birthday
    )
  });
})

app.post('/setApprover', async function (req, res) {
  res.json({
    data: await instance.setApprover.sendTransaction(
      req.body.filename,
      req.body.approver_id,
      req.body.encrypted_secret_share,
      {from: req.body.user_id}
    )
  });
})


app.get('/getApproverSecret', async function (req, res) {
  res.json({
    data: await instance.getApproverSecret.call(
      req.query.filename,
      req.query.approver_id
    )
  });
})

app.post('/requestFile', async function (req, res) {
  res.json({
    data: await instance.requestFile.sendTransaction(
      req.body.filename,
      {from: req.body.user_id}
    )
  });
})

app.get('/getApprovableList', async function (req, res) {
  var results = await instance.getApprovableList.call(
      {from: req.query.user_id}
    );
  res.json({
    data: str2array(results, ";")
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
