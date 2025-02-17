pragma solidity >=0.4.21 <0.7.0;

contract AccessLog {



/************************************************************************************ 
*                                                                                   *
*   Defaults                                                                        *
*                                                                                   *
************************************************************************************/

    address private owner;
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
    

/************************************************************************************ 
*                                                                                   *
* Part 1: Initial User Creation Related Functions                                   *
*                                                                                   *
************************************************************************************/
    mapping(address => string) files;
    mapping(address => bool) private hasFile;
    
    mapping(address => string) publicKeys;
    mapping(uint => string) publicKeysId;
    mapping(uint => address) ethereum_address_dict;

    // API 7
    function setPublicKey (string memory _publicKey) public {
        publicKeys[msg.sender] = _publicKey;
    }
    function setPublicKeyWithName (string memory username, string memory birthday, string memory _publicKey) public {
        require(keccak256(abi.encodePacked(publicKeys[msg.sender])) == keccak256(abi.encodePacked(_publicKey)));
        publicKeysId[getUserName(username, birthday)] = _publicKey;
        // maybe can update here
        ethereum_address_dict[getUserName(username, birthday)] = msg.sender;
    }

    // API 2
    /**
    Gets the public key associated with a user
    @param username the username of the specified user
    @param birthday the birthday of the user user
    @return the public key associated with <username, birthday>
    */
    function getPublicKeyWithName(string memory username, string memory birthday) public view returns (string memory) {
        return publicKeysId[getUserName(username,birthday)];
    }
    function getPublicKey() public view returns (string memory) {
        return publicKeys[msg.sender];
    }

    // API 9: Get Ethereum address with User's name and birthday
    function getEthereumAdress(string memory username, string memory birthday) public view returns (address) {
         return ethereum_address_dict[uint(keccak256(abi.encodePacked(username,birthday)))];
    }
    // API 10: Associated a username with Ethereum Address
    function setEthereumAdress(string memory username, string memory birthday ) public {
        ethereum_address_dict[getUserName(username,birthday)] = msg.sender;
    }

    function getUserName(string memory username, string memory birthday) public pure returns (uint)  {
        return uint(keccak256(abi.encodePacked(username, birthday)));
    }


/************************************************************************************ 
*                                                                                   *
* Part 2: File manipulation with user id                                            *
*                                                                                   *
************************************************************************************/
    // API 1/12: Adding a file to the list that is corresponding to the user
    function addFilename(string memory fileName) public {
        hasFile[msg.sender] = true;
        string memory temp = append(fileName,";");
        files[msg.sender] = append(files[msg.sender], temp);
    }

    // API 8
    // Getting a "list" of file names: a list string that is separated with new line character
    function getFiles(address _address) public view returns (string memory) {
        // Caller must have a file asscoiated with it
        assert(hasFile[_address]);
        return files[_address];
    }

    // API 13: Remove a file from that user
    function removeFile(string memory filename) public {
        // Checks if this user contain the specified filename
        assert(contains(filename, files[msg.sender]));
        // Find the index of the substring, remove the substring
        filename = append(filename,";");
        files[msg.sender] = remove(filename, files[msg.sender]);

    }

    // Helper function to join two strings
    function append(string memory a, string memory b) internal pure returns (string memory) {
        return string(abi.encodePacked(a, b));
    }

    // When user tries to access a file, they must call this function to log their accesses
    function log(uint file) public payable {
        // Caller must have a file asscoiated with it
        assert(hasFile[msg.sender]);
        emit Log(msg.sender, file);
    }

    // Helper function to find a substring
    function contains (string memory target, string memory base) internal pure returns (bool) {
        bytes memory targetBytes = bytes (target);
        bytes memory baseBytes = bytes (base);

        bool found = false;

        // Loop through the original string
        for (uint i = 0; i <= baseBytes.length - targetBytes.length; i++) {
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
    function remove(string memory target, string memory base) internal pure returns (string memory) {
        bytes memory targetBytes = bytes (target);
        bytes memory baseBytes = bytes (base);

        uint index = 0;
        // Loop through the original string
        for (uint i = 0; i <= baseBytes.length - targetBytes.length; i++) {
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
        return string(abi.encodePacked(substring(base,0,index), substring(base, index + targetBytes.length, baseBytes.length )));
 
    }
    // Helper function for removing a file from list string
    function substring(string memory str, uint startIndex, uint endIndex) internal pure returns (string memory) {
        bytes memory strBytes = bytes(str);
        bytes memory result = new bytes(endIndex-startIndex);
        for(uint i = startIndex; i < endIndex; i++) {
            result[i-startIndex] = strBytes[i];
        }
        return string(result);
    }

/******************************************************************************** 
*                                                                               *
* Part 3: Setting up secret shares                                              *
*                                                                               *
********************************************************************************/
    
    struct File {
        address[] approvers;
        mapping(address => string) secrets_shares;
    }
    mapping(string => File) approval_dict;

    // API 3: Establish a mapping for a file name and an approver
    function setApprover(string memory filename, address approverId, string memory encrypted_secret_share) public returns (string memory) {

        bool exisit = false;
        // Check if the associated user is alredy in the list of approvers
        for (uint i = 0; i < approval_dict[filename].approvers.length; i++){
            if (approval_dict[filename].approvers[i] == approverId) {
               exisit = true;
               break;
            }
        }
        if (exisit == false) {
            approval_dict[filename].approvers.push(approverId);
        }

        // Updating an exisiting account with a new encrypted_secret_share
        approval_dict[filename].secrets_shares[approverId] = encrypted_secret_share;
        return "Success";
    }

    // API 5: Get encrypted secret share with approver's public key
    function getApproverSecret(string memory filename, address approverId) public view returns (string memory) {
        return approval_dict[filename].secrets_shares[approverId];
    }


/******************************************************************************** 
*                                                                               *
* Part 4: Requsting a file                                                      *
*                                                                               *
********************************************************************************/

    struct Request {
        string filename;
        address requester;
        uint timestamp;
    }
    mapping(address => Request[]) request_board_dict;
    Request[] request_board;

    // API 11: Putting in a request for a file
    function requestFile(string memory _filename) public returns (string memory) {

        Request memory new_request = Request({filename: _filename, requester:msg.sender, timestamp: now});

        // Adding request to request board
        request_board.push(new_request);
        request_board_dict[msg.sender].push(new_request);

        return "Successfully added request to request board";

    }

    function toString(address _addr) public pure returns(string memory)
    {
        bytes32 value = bytes32(uint256(_addr));
        bytes memory alphabet = "0123456789abcdef";

        bytes memory str = new bytes(51);
        str[0] = '0';
        str[1] = 'x';
        for (uint256 i = 0; i < 20; i++) {
            str[2+i*2] = alphabet[uint8(value[i + 12] >> 4)];
            str[3+i*2] = alphabet[uint8(value[i + 12] & 0x0f)];
        }
        return string(str);
    }

    function uint2str(uint _i) internal pure returns (string memory _uintAsString) {
    if (_i == 0) {
        return "0";
    }
    uint j = _i;
    uint len;
    while (j != 0) {
        len++;
        j /= 10;
    }
    bytes memory bstr = new bytes(len);
    uint k = len - 1;
    while (_i != 0) {
        bstr[k--] = byte(uint8(48 + _i % 10));
        _i /= 10;
    }
    return string(bstr);
}

//    // API 4: check the request board and see which one I can approve
//    function getApprovableList() public view returns (string memory) {
//        
//        string memory approval_list = "";
//        for(uint i = 0; i < request_board.length; i++ ){
//            string memory _filename  = request_board[i].filename;
//            address[] memory approver_list = approval_dict[_filename].approvers;
//            bool found = false;
//            uint index = 0;
//            for(uint j = 0; j < approver_list.length; j++ ){
//                if (approver_list[j] == msg.sender) {
//                    found  = true;
//                    index = i;
//                }
//            }
//            if (found){
//                approval_list = append(approval_list, _filename);
//                approval_list = append(approval_list, '+');
//                approval_list = append(approval_list, toString(request_board[index].requester));
//                approval_list = append(approval_list, '+');
//                approval_list = append(approval_list,uint2str(request_board[index].timestamp));
//                approval_list = append(approval_list, ";");
//            }
//        }
//        return approval_list;
//    }
    // API 4: check the request board and see which one I can approve
    function getApprovableList() public view returns (string memory) {
        
        string memory approval_list = "";
        for(uint i = 0; i < request_board.length; i++ ){
            string memory _filename  = request_board[i].filename;

            address[] memory approver_list = approval_dict[_filename].approvers;
            bool found = false;
            uint index = 0;
            for(uint j = 0; j < approver_list.length; j++ ){
                if (approver_list[j] == msg.sender) {
                    found  = true;
                    index = i;
                }
            }
            if (found){

                // Check if this file is on approved board

                //Approval[] memory approved_list = approval_board;
                bool approved_before = false;
                for(uint k = 0; k < approval_board.length; k++ ){
                    if (approval_board[k].approver == msg.sender) {
                        string memory left = approval_board[k].filename;
                        if (keccak256(abi.encodePacked(left)) == keccak256(abi.encodePacked(_filename))) {
                            approved_before = true;
                        }
                    }
                }
                if (!approved_before) {
                    approval_list = append(approval_list, _filename);
                    approval_list = append(approval_list, '+');
                    approval_list = append(approval_list, toString(request_board[index].requester));
                    approval_list = append(approval_list, '+');
                    approval_list = append(approval_list,uint2str(request_board[index].timestamp));
                    approval_list = append(approval_list, ";");
                 }
           }
        }

        return approval_list;
    }

    struct Approval {
        string filename;
        address requester;
        address approver;
        string encrypted_secret;
        uint timestamp;
    }
    mapping(address => Approval[]) approval_board_dict;
    Approval[] approval_board;

    // API 6: Approving a file
    function approve(string memory _filename, address _requester, string memory _encrypted_share) public returns (string memory) {
    
        Approval memory temp = Approval({filename: _filename, requester: _requester, approver: msg.sender, encrypted_secret: _encrypted_share, timestamp: now});
        approval_board.push(temp);
        approval_board_dict[msg.sender].push(temp);
        return "Approved and added to the approve board";
    }




    // API 14: get list of files and encrypted secret share that I requested
    function getApprovedListSecrets() public view returns (string memory) {
        string memory approval_list_result = "";
        for(uint i = 0; i < approval_board.length; i++ ){

            // If I am the requester of this Approval item
            if (approval_board[i].requester == msg.sender) {
                approval_list_result = append(approval_list_result, approval_board[i].filename);
                approval_list_result = append(approval_list_result, ":");
                approval_list_result = append(approval_list_result, approval_board[i].encrypted_secret);
                approval_list_result = append(approval_list_result, ";");

            }
        }

        return approval_list_result;
    }


}
