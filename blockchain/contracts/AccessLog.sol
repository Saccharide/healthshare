pragma solidity >=0.4.21 <0.7.0;

contract AccessLog {
    address private owner;
    mapping(address => string) files;
    mapping(address => bool) private hasFile;
    
    // mapping(address)
    event Log(
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

    function getFilename(string memory patientName, string memory birthday) public pure returns (uint)  {
        return keccak256(abi.encodePacked(patientName, birthday));
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

    // Getting a "list" of file names: a list string that is separated with new line character
    function getFiles() public returns (string) {

        // Caller must have a file asscoiated with it
        assert(hasFile[msg.sender]);
        return files[msg.sender];
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

        // Find the index of the substring

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
}
