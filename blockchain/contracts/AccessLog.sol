pragma solidity >=0.4.21 <0.7.0;

contract AccessLog {
  address private owner;
  mapping(address => [])
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

  function getFilename(String memory patientName, String memory birthday) public pure returns (uint256)  {
      return keccak256(patientName, birthday);
  }

  function log(uint file) public payable {
      require()
      emit Log(msg.sender, file);
  }
}
