pre-requisites:
```
➤ node --version
v12.9.1
➤ npm --version
6.11.2
➤ python --version
Python 3.7.4
➤ pip freeze | grep requests
requests==2.22.0
```

```
npm install -g truffle@5.1.13  # may need sudo
cd blockchain   # same dir as this README.md
npm install
truffle compile     # should show successful compilation
truffle develop     # this launches a local blockchain, should show 10 different accounts
> migrate --reset   # run within truffle develop console
```

Open another terminal
``` 
cd blockchain
node server.js      # should show listening on port 3000
```

Open another terminal

``` 
cd blockchain
python test.py      # should show all testcases passed
```

Also refer to test.py for sample usage

