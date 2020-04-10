var Web3 = require("web3");
var Web3 = require('web3');

var provider = new Web3.providers.HttpProvider("http://localhost:9545");
var web3 = new Web3(provider);
var contract = require("@truffle/contract");

var AccessLog = contract(require("./build/contracts/AccessLog.json"))

const express = require('express')
var bodyParser = require('body-parser')

const asyncHandler = require('express-async-handler')

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

function timestamp2str(ts) {
  var date = new Date(ts * 1000);
  return (date.getMonth()+1) + "/"
    + date.getDate() + "/"
    + date.getFullYear() + " "
    + date.getHours() + ":"
    + date.getMinutes() + ":"
    + date.getSeconds();
}

async function main() {
  accounts = await web3.eth.getAccounts();
  AccessLog.setProvider(provider);
  instance = await AccessLog.deployed();
  console.log("Server listening on port 3000");
  app.listen(3000)
}

app.get('/getPublicKey', asyncHandler(async function (req, res) {
  res.json({
    data: await instance.getPublicKey.call({from: req.query.user_id})
  });
}))

app.post('/setPublicKey', asyncHandler(async function (req, res) {
  res.json({
    data: await instance.setPublicKey.sendTransaction(req.body.public_key, {from: req.body.user_id})
  });
}))

app.post('/addFile', asyncHandler(async function (req, res) {
  res.json({
    data: await instance.addFilename.sendTransaction(
      req.body.file_name,
      {from: req.body.user_id}
    )
  });
}))

app.get('/getFiles', asyncHandler(async function (req, res) {
  var address = (req.query.user_id);
  res.json({
    data: str2array(await instance.getFiles.call(address))
  });
}))

app.post('/setDetails', asyncHandler(async function (req, res) {
  var address = req.body.user_id;
  res.json({
    data: await instance.setEthereumAdress.sendTransaction(
      req.body.name,
      req.body.birthday,
      {from: address}
    )
  });
}))


app.get('/getAddressFromDetails', asyncHandler(async function (req, res) {
  res.json({
    data: await instance.getEthereumAdress.call(
      req.query.name,
      req.query.birthday
    )
  });
}))

app.post('/setApprover', asyncHandler(async function (req, res) {
  res.json({
    data: await instance.setApprover.sendTransaction(
      req.body.filename,
      req.body.approver_id,
      req.body.encrypted_secret_share,
      {from: req.body.user_id}
    )
  });
}))


app.get('/getApproverSecret', asyncHandler(async function (req, res) {
  res.json({
    data: await instance.getApproverSecret.call(
      req.query.filename,
      req.query.approver_id
    )
  });
}))

app.get('/getApprovableList', asyncHandler(async function (req, res) {
  var results = await instance.getApprovableList.call(
      {from: req.query.user_id}
    );

  results = str2array(results, ";")
  results = results.map((data) => {
    let procesed_data = str2array(data, "+")
    return {
      "filename": procesed_data[0].replace(/\0/g, ''),
      "requestor_id": procesed_data[1].replace(/\0/g, ''),
      "datetime": timestamp2str(parseInt(procesed_data[2].replace(/\0/g, '')))
    }
  })

  res.json({
    data: results
  });
}))

app.post('/requestFile', asyncHandler(async function (req, res) {
  res.json({
    data: await instance.requestFile.sendTransaction(
      req.body.filename,
      {from: req.body.user_id}
    )
  });
}))

app.post('/approve', asyncHandler(async function (req, res) {
  res.json({
    data: await instance.approve.sendTransaction(
      req.body.filename,
      req.body.requestor,
      req.body.encrypted_share,
      {from: req.body.user_id}
    )
  });
}))

app.get('/getApprovedListSecrets', asyncHandler(async function (req, res) {
  var results = await instance.getApprovedListSecrets.call(
      {from: req.query.user_id}
    );
  results = str2array(results, ";")
  results = results.map((data) => {
    let procesed_data = str2array(data, ":")
    return {
      "filename": procesed_data[0],
      "secret_share": procesed_data[1],
    }
  })
  res.json({
    data: results
  });
}))

app.post('/removeFile', asyncHandler(async function (req, res) {
  res.json({
    data: await instance.removeFile.sendTransaction(
      req.body.filename,
      {from: req.body.user_id}
    )
  });
}))


app.post('/createAccount', asyncHandler(async function (req, res) {
  let acc = await web3.eth.accounts.wallet.create(1);
  res.json({
    data: {
      "address": acc[0].address,
      "privateKey": acc[0].privateKey
    }
  });
}))

app.use(function(err, req, res, next) {
  console.log(err);
  return res.status(500).json({
    "error": err
  });
});

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
