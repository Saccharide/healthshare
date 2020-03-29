var contractABI = [
    {
      "inputs": [
        {
          "internalType": "bytes32[]",
          "name": "_candidateList",
          "type": "bytes32[]"
        }
      ],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "creator",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "str",
          "type": "bytes32"
        }
      ],
      "name": "bytes32ToString",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "payable": false,
      "stateMutability": "pure",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "bytes32",
          "name": "_candidate",
          "type": "bytes32"
        }
      ],
      "name": "vote",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "string",
          "name": "_candidate",
          "type": "string"
        }
      ],
      "name": "vote",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [],
      "name": "closeVote",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [],
      "name": "reopenVote",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "getWinner",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    }
  ];
const contractAddress = '0x732bc1a64ad6dC0e1648B498105C01FCE1695483';
const web3 = new Web3('http://localhost:9545');
const votingContract= new web3.eth.Contract(contractABI, contractAddress);

//console.log(votingContract)
//
//web3.eth.getAccounts()
//.then(console.log);

//votingContract.methods.vote("candidate 1").call().then(() => {
//    console.log(votingContract.winner);
//    console.log(votingContract.max_vote);
//    console.log("finished voting");
//});
//votingContract.methods.closeVote().call().then((_winner, _votes) => {
//            console.log(_winner);
//            console.log(_votes);
//        });
document.addEventListener('DOMContentLoaded', () => {
    const $candidateName = document.getElementById('candidate-name');
    const $voteButton = document.getElementById("vote");
    const $winner = document.getElementById('winner');
    const $votes  = document.getElementById('max-votes');

    let accounts = [];
    // populate test accounts
    web3.eth.getAccounts()
        .then(_accounts => {
            accounts = _accounts;
        });

    //
    const getWinner = () => {
        votingContract.methods.closeVote().call().then((_winner, _votes) => {
            console.log(_winner);
            console.log(_votes);
            $winner.innerHTML = _winner;
            $votes.innerHTML = _votes;
        });
    };

    getWinner();
    $voteButton.addEventListener('submit', e => {
        e.preventDefault();
        const name = e.target.elements[0].value;
        console.log("name entered : "+name);
        votingContract.methods.vote(name).send({from: accounts[0]}).then(getWinner);
    });

});
