pragma solidity >=0.4.21 <0.7.0;

contract AccessLog {
  address private owner;

  event Log(
          address caller,
          uint file
          );

  constructor() public {
    owner = msg.sender;
  }

  modifier isOwner() {
    require(msg.sender == owner);
    _;
  }


  function log(uint file) public payable {
      emit Log(msg.sender, file);
  }
}
