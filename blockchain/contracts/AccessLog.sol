pragma solidity >=0.4.21 <0.7.0;

contract AccessLog {

    address private owner;
    mapping(address => string) files;
    mapping(address => bool) private hasFile;
    
    mapping(address => string) publicKeys;
    mapping(uint => string) publicKeysId;
    function setPublicKey (string memory _publicKey) {
        publicKeys[msg.sender] = _publicKey;
    }
    function setPublicKeyWithName (string memory username, string memory birthday, string memory _publicKey) {
        require(publicKeys[msg.sender] == _publicKey)
        publicKeys[getUserName(username, birthday)] = _publicKey;
    }

    // API 2
    function getPublicKey() returns (string) {
        return publicKeys[msg.sender];
    }
    function getPublicKeyWithName(string memory username, string memory birthday) returns (string) {
        return publicKeysId[getUserName(username,birthday)];
    }


    // mapping(address)
    event Log(
        uint timestamp,
        address caller,
        uint file
    );

    constructor() public {
        owner = msg.sender;
    }

    // Check if caller is owner of the contract
    modifier isOwner() {
        require(msg.sender == owner);
        _;
    }

    function getUserName(string memory username, string memory birthday) public pure returns (uint)  {
        return keccak256(abi.encodePacked(username, birthday));
    }

    // Adding a file to the list that is corresponding to the user
    function addFilename(string memory fileName) public {
        hasFile[msg.sender] = true;
        string memory temp = append("\n", fileName);
        files[msg.sender] = append(files[msg.sender], temp);
    }

    // Helper function to join two strings
    function append(string memory a, string memory b) internal pure returns (string) {
        return string(abi.encodePacked(a, b));
    }

    // API 1
    // Getting a "list" of file names: a list string that is separated with new line character
    function getFiles(address _address) public returns (string) {
        // Caller must have a file asscoiated with it
        assert(hasFile[_address]);
        return files[_address];
    }

    // When user tries to access a file, they must call this function to log their accesses
    function log(uint file) public payable {
        // Caller must have a file asscoiated with it
        assert(hasFile[msg.sender]);
        emit Log(msg.sender, file);
    }

    // Remove a file from that user
    function removeFile(string memory filename) public {
        
        // Check if this user has anyfile at all
        assert(hasFile[msg.sender]);

        // Checks if this user contain the specified filename
        assert(contains(filename, files[msg.sender]));

        // Find the index of the substring, remove the substring
        remove(filename, files[msg.sender]);

    }

    // Helper function to find a substring
    function contains (string memory target, string memory base) internal view returns (bool) {
        bytes memory targetBytes = bytes (target);
        bytes memory baseBytes = bytes (base);

        bool found = false;

        // Loop through the original string
        for (uint i = 0; i < baseBytes.length - targetBytes.length; i++) {
            bool flag = true;
            // Check each character to see if they match
            for (uint j = 0; j < targetBytes.length; j++){ 
                if (baseBytes [i + j] != targetBytes [j]) {
                    flag = false;
                    break;
				}
			}
            if (flag) {
                found = true;
                break;
            }
        }
        return found;
    }

    // Helper function to remove a filename from list of filenames, basically remove a substring from base string
    function remove(string memory target, string memory base) internal view returns (string memory) {
        bytes memory targetBytes = bytes (target);
        bytes memory baseBytes = bytes (base);


        uint index = 0;
        // Loop through the original string
        for (uint i = 0; i < baseBytes.length - targetBytes.length; i++) {
            bool flag = true;
            // Check each character to see if they match
            for (uint j = 0; j < targetBytes.length; j++){ 
                if (baseBytes [i + j] != targetBytes [j]) {
                    flag = false;
                    break;
				}
			}
            if (flag) {
                index = i;
                break;
            }
        }
        return string(abi.encodePacked(substring(base,0,index), substring(base,baseBytes.length - targetBytes.length, baseBytes.length )));
 
    }
    // Helper function for removing a file from list string
    function substring(string str, uint startIndex, uint endIndex) constant returns (string) {
        bytes memory strBytes = bytes(str);
        bytes memory result = new bytes(endIndex-startIndex);
        for(uint i = startIndex; i < endIndex; i++) {
            result[i-startIndex] = strBytes[i];
        }
        return string(result);
    }
}
