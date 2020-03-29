### Example Scenario
File owner: Tony
File approvers: Elgin, Tony, Harrison
You need 2 people to approve

TonyFile.zip
secret key: 123456789
secret shares: [123,456,789]

Elgin = 123 (encrypted with Elgin public key) -> encrypted_secret_share_Elgin
Tony = 456 (encrypted with Tony public key) -> encrypted_secret_share_Tony
Harrison = 789 (encrypted with Harrison public key) -> encrypted_secret_share_Harrison

Quang requests for file (need 2 approving)
What Quang needs: any of the two in [123,456,789]

Elgin fetches encrypted_secret_share_Elgin from smart contract 2
decrypts encrypted_secret_share_Elgin to get [123]
encrypt [123] to get encrypted_secret_shares_encrypted_Quang
put this on smart contract 4

Tony fetches encrypted_secret_share_Tony from smart contract 2
decrypts encrypted_secret_share_Tony to get [456]
encrypt [456] to get encrypted_secret_shares_encrypted_Quang
put this on smart contract 4

Quang gets both encrypted_secret_shares_encrypted_Quang
Decrypts both encrypted_secret_shares_encrypted_Quang to get [123],[456]
Recreates secret key 123456789
Decrypts file


### Smart Contracts

Smart contract 1: <user,birthdate> -> p2pFilename
e.g <Tony,01/01/2020> -> 45678afaghsjda5yui6789

Smart contract 2: p2pFileName -> <approver_userid,encrypted_secret_shares_with_approver_public_key>
e.g.
45678afaghsjda5yui6789 -> <Elgin, encrypted_secret_share_Elgin>
45678afaghsjda5yui6789 -> <Tony, encrypted_secret_share_Tony>
45678afaghsjda5yui6789 -> <Harrison, encrypted_secret_share_Harrison>

Smart contract 3: (requests smart contract): p2pFileName -> requestor_userid
e.g
45678afaghsjda5yui6789 -> Quang

Smart contract 4: p2pFileName -> <approver_userid, requester_userid, encrypted_secret_shares_encrypted_with_requestor_public_key>
e.g.
45678afaghsjda5yui6789 -> <Elgin, Quang, [123], signatureOfMessagewithElginsPrivateKey>
45678afaghsjda5yui6789 -> <Tony, Quang, [456], signatureOfMessagewithElginsPrivateKey>

Smart contract 5: which files I can approve
Elgin -> 45678afaghsjda5yui6789
Tony -> 45678afaghsjda5yui6789
Harrison -> 45678afaghsjda5yui6789

Smart contract 6: user to public key mapping
Elgin -> Elgin_Public_Key
Tony -> Tony_Public_Key
Harrison -> Harrison_Public_Key
Quang -> Quang_Public_Key

### APIs Needed

API 1: create mapping between
	input: whatever authentication information you need <user, user birthdate>
	output: List of p2pFileNames

API 2: fetch public key of user
	input: user_id
	output: user_public_key

API 3: create approval mappings (who can approve the newly created file)
	input: p2pFileName, approval_user_id, encrypted_secret_share_approver_user_id
	output: (updates smart contract 2 and 5) status message
	
API 4: check if pending approval requests (goes to smart contract 5 and queries smart contract 3 and checks against smart contract 4 if it has ALREADY been approved)
	input: -
	output: status message

API 5: get encrypted_secret_shares_with_approver_public_key
	input: p2pFileName, approver_userid
	output: encrypted_secret_shares_with_approver_public_key
	
API 6: approve request
	input: p2pFileName, approver_userid, requester_userid, encrypted_secret_shares_encrypted_with_requestor_public_key
	output: status message
	
API 7: create public key of user
	input: user_id, public_key
	output: status message
# HealthShare
HealthShare is a POC for securely sharing patient-provided information among patients, providers, and various healthcare organizations. Although standards like Fast Healthcare Interoperability Resources (FHIR) exist for uniformly encoding patient data, there isn't a uniform or consistent platform to data from a consumer/patient standpoint. HealthShare aims to fill in that gap using a structured P2P, encrypted file sharing system backed by Blockchain technology to guarantee data authenticity and integrity. Built using OpenDHT, Ethereum, and Truffle, Healthshare is the result of Quang Huynh, Tony Tang, Elgin Lee Wei Sheng, and Harrison Banh from the Georgia Institute of Technology as their class project for Professor Ling Liu's CS 6675 Advanced Internet Computing class. 

## Setup and Usage Instructions
### I. OpenDHT
#### Installation
  **1) Install OpenDHT dependencies**
  
    sudo apt install libncurses5-dev libreadline-dev nettle-dev libgnutls28-dev libargon2-0-dev libmsgpack-dev librest

  **2) Install python binding dependencies**
  
    sudo apt-get install cython3 python3-dev python3-setuptools

  **3) Install asio.hpp**
  
    wget https://github.com/aberaud/asio/archive/b2b7a1c166390459e1c169c8ae9ef3234b361e3f.tar.gz \
    && tar -xvf b2b7a1c166390459e1c169c8ae9ef3234b361e3f.tar.gz && cd asio-b2b7a1c166390459e1c169c8ae9ef3234b361e3
    && ./autogen.sh && ./configure --prefix=/usr --without-boost --disable-examples --disable-tests \
    && sudo make install

  **4) Install Git directory**

    git clone https://github.com/savoirfairelinux/opendht.git

  **5) Build and Install**

    cd opendht
    mkdir build && cd build
    cmake -DOPENDHT_PYTHON=ON -DCMAKE_INSTALL_PREFIX=/usr ..
    make -j4
    sudo make install

#### Usage
  **Running a node**

    dhtnode

  **specify a bootstrap node address (can be any running node of the DHT network)**

    dhtnode -b

  **Put a key value pair**

    $ p [key] [value]

  **Search for a key**

    $ q [key]
