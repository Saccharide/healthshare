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
    
### II. Healthshare's Custom Cryptography Wrapper
#### Installation
 **1) Install pip**
 
 	sudo apt-get install python python-pip
	
 **2) Install our secret sharing module**
 
 	sudo pip install secretsharing
	
#### Usage 
	python2 main.py

## Design and Example Scenario
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


API 8: Get list of filenames associated with user
	input: Username, Birthday or Ethereum address
	output: A list of p2pFilenames in the form of one single string

To better illustrate and show the design of Healthshare, let us examine the following scenario. Say that we have our patient, Tony, who has authorized his friends Elgin and Harrison as secret share holders. Our system will represent Tony as the following...
### System Setup

  **1) File Owner and Immediate Trusted Parties**
  
  - **File owner :** Tony 
  - **File approvers:** Elgin, Tony, Harrison where 2 out of the 3 share owners are required to grant access to Tony's file
    
  **2) File and Related Cryptographic Details**  
  - **File :** TonyFile.zip
  - **Secret Key :** 123456789
  - **Secret Shares:** [123,456,789
    - **Elgin =** 123 (encrypted with Elgin public key) -> encrypted_secret_share_Elgin
    - **Tony =** 456 (encrypted with Tony public key) -> encrypted_secret_share_Tony 
    - **Harrison =** 789 (encrypted with Harrison public key) -> encrypted_secret_share_Harrison
 
 ### Granting Example
 #### Quang's Request
Quang, a 3rd party, wants and requests for access to Tony's file. To gain access, Quang needs any of the two shares in [123,456,789]. The system logs Quang's request and sends notifications to the share owners : Tony, Elgin, and Harrison asking them if they will both approve and grant Quang's access.

#### Approving Share Owners
  **1) Elgin approves of Quang** 
  
   - Elgin fetches his own secret share, encrypted_secret_share_Elgin, from *Smart Contract 2*
   - Decrypts his own secret share to get [123] and 
   - Then he re-encrypts [123] under Quang's public key to get encrypted_secret_shares_encrypted_Quang and stores the result in this in 	*Smart Contract 4*

  **2) Tony also approves of Quang**
  
   - Tony fetches also fetches his own share, encrypted_secret_share_Tony, from *Smart Contract 2*
   - Decrypts encrypted_secret_share_Tony to get [456] and 
   - Then re-encrypts [456] under Quang's public key to get encrypted_secret_shares_encrypted_Quang and simlarly, stoers the result in *Smart Contract 4*
  
  At this point, 2 of out of the 3 share owners have approved of Quang granting him access to Tony's file. It is no longer necessary for Harrison to approve of Quang. However, he can still approve of Quang if he desires to choose so, but as far as Quang is concerned, he now has access to Tony's file which is all that matters to him.

#### Quang gets Access
Once Tony and Elgin have approved and sent their secret shares to Quang, Quang sees <Tony, encrypted_secret_shares_encrypted_Quang> and <Elgin, encrypted_secret_shares_encrypted_Quang>. Using his secret key, he is able to decrypt both and receive [123] and [456] from Tony and Elgin respectively. Now holding the required 2 out of 3 shares, Quang is able to recreate and use the secret key, 123456789, to gain access to Tony's file. 
