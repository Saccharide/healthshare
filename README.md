# HealthShare <a name="intro"></a>
---
HealthShare is a POC for securely sharing patient-provided information among patients, providers, and various healthcare organizations. Although standards like Fast Healthcare Interoperability Resources (FHIR) exist for uniformly encoding patient data, there isn't a uniform or consistent platform to data from a consumer/patient standpoint. HealthShare aims to fill in that gap using a structured P2P, encrypted file sharing system backed by Blockchain technology to guarantee data authenticity and integrity. Built using OpenDHT, Ethereum, and Truffle, HealthShare is the result of Quang Huynh, Tony Tang, Elgin Lee Wei Sheng, and Harrison Banh from the Georgia Institute of Technology as their class project for Professor Ling Liu's CS 6675 Advanced Internet Computing class. 

## Table of contents
- [What is HealthShare?](#intro)
- [Setup and Usage Instructions](#setup-and-usage-instructions)
  1. [OpenDHT](#opendht)
     1. [Installation](#opendht_installation)
     1. [Usage](#opendht_usage)
  1. [Custom Crypto Wrapper](#healthshare_crypto_wrapper)
     1. [Installation](#healthshare_crypto_wrapper_installation)
     1. [Usage](#healthshare_crypto_wrapper_usage)
  1. [Truffle](#truffle)
     1. [Installation](#truffle_installation)
     1. [Usage](#truffle_usage)
- [Design and Example Scenario](#design-and-example-scenario)
  1. [Smart Contracts](#smart_contracts)
  1. [APIs](#apis)
  1. [Use Case Example](#use_case_example)

## Setup and Usage Instructions 
### I. OpenDHT <a name="opendht"></a>
---
#### Installation <a name="opendht_installation"></a>
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

#### Usage <a name="opendht_usage"></a>
  **Running a node**

    dhtnode

  **specify a bootstrap node address (can be any running node of the DHT network)**

    dhtnode -b

  **Put a key value pair**

    $ p [key] [value]

  **Search for a key**

    $ q [key]
    
### II. HealthShare's Custom Cryptography Wrapper <a name="healthshare_crypto_wrapper"></a>
---
#### Installation <a name="healthshare_crypto_wrapper_installation"></a>
 **1) Install pip**
 
 	sudo apt-get install python python-pip
	
 **2) Install our secret sharing module**
 
 	sudo pip install secretsharing
	
#### Usage <a name="healthshare_crypto_wrapper_usage"></a>
	python2 main.py
	
### III. Truffle <a name="truffle"></a>
---
#### Installation <a name="truffle_installation"></a>
 **1) Install node and npm**
 	
	sudo apt-get install nodejs 
	
 **2) Install freeze**
 
 	sudo pip install freeze

 **3) Install requests**
 
 	sudo pip install requests

 **4) Install Truffle**
 
 	sudo npm install -g truffle@5.1.13

#### Usage <a name="truffle_usage"></a>
  **1) Switch into the "blockchain" directory of this project**
  	
	cd blockchain
	
  **2) Run npm install**
  
  	npm install 
	
  **3) Compile Truffle** 
  	
	truffle compile     # should show successful compilation
	
  **4) Launch Truffle**
 		
	truffle develop	    # this launches a local blockchain, should show 10 different accounts
	> migrate --reset   # run within truffle develop console

  **5) Verify that Truffle is Running**
 
 Open a new terminal and do the following
		
	cd blockchain
	node server.js	    # should show listening on port 3000
		
Open a second terminal and do the following 
	
	cd blockchain       # replace ACCOUNT_0 in test.py with one of the 10 accounts above
	python test.py      # should show all testcases passed

Refer to blockchain/test.py for more on sample usage, and https://github.com/Saccharide/playing-with-truffle for information on the development process.
		
		
## Design and Example Scenario
HealthShare uses a series of Smart Contracts and API's to communicate between our file sharing P2P network and system log Block chains. 

### I. Smart Contracts <a name="smart_contracts"></a>
---
  **Smart Contract 1 (HealthShare User) : <user,birthdate> -> p2pFilename**
  
  This smart contract associates a HealthShare user to encrypted patient file in the P2P network. For simplicity sake, the user's file is a hash of their name and birthday which we assume to be unique.
  	
	<Tony,01/01/2020> -> 45678afaghsjda5yui6789

  **Smart Contract 2 (Share Owners) : p2pFileName -> <approver_userid, encrypted_secret_shares_with_approver_public_key>**
  
  Smart Contract 2 both stores and represents the share owners of a patient file. It holds a mapping of the hashed P2P file name to name of the share owner and their encrypted share. 
  
	45678afaghsjda5yui6789 -> <Elgin, encrypted_secret_share_Elgin>
	45678afaghsjda5yui6789 -> <Tony, encrypted_secret_share_Tony>
	45678afaghsjda5yui6789 -> <Harrison, encrypted_secret_share_Harrison>

  **Smart Contract 3 (Requests Smart Contract) : p2pFileName -> requestor_userid**
  
  Smart Contract 3 stores a mapping of hashed P2P file names to users who want to get access to that file.
  
	45678afaghsjda5yui6789 -> Quang

  **Smart Contract 4 (Approved Requesting Users) : p2pFileName -> <approver_userid, requester_userid, encrypted_secret_shares_encrypted_with_requestor_public_key>**
  
  Smart Contract 4 stores the data regarding approved requests for a file. It maps the hashed P2P file name to a tuple of A) the user id of the approver B) the user id of the requestor and C) the secret share of the approver encrypted under the requestor's public key 
  
	45678afaghsjda5yui6789 -> <Elgin, Quang, [123], signatureOfMessagewithElginsPrivateKey>
	45678afaghsjda5yui6789 -> <Tony, Quang, [456], signatureOfMessagewithElginsPrivateKey>

  **Smart Contract 5 (Share Owner's Files) : user id -> p2pFileName**
  
  Smart Contract 5 stores a list of patient files in which the user owns a share for. It is used in between Contracts 3 and 4 to grant a requesting user access to a patient file 
  
	Elgin -> 45678afaghsjda5yui6789
	Tony -> 45678afaghsjda5yui6789
	Harrison -> 45678afaghsjda5yui6789

  **Smart Contract 6 (Key Store) : user id -> public key**

  Smart Contract 6 functions as a key store. It relates a user id with their public key. 
  
	Elgin -> Elgin_Public_Key
	Tony -> Tony_Public_Key
	Harrison -> Harrison_Public_Key
	Quang -> Quang_Public_Key

### II. APIs Needed <a name="apis"></a>
---
  **API 1 : Associating User Information**
  
  
  Creates and links a patient file with user's id (an address)

	input: user_address, file_name
	output: <none>

  **API 2 : Fetching a User's Public Key**
  
  
  Gets the public key associated with a user 

	input: user_id
	output: user_public_key

  **API 3: Approval Mappings**
  

  Determines who can approve a patient file 
  
	input: p2pFileName, user_id, approval_user_id, encrypted_secret_share_approver_user_id
	output: (updates smart contract 2 and 5) status message
	
  **API 4 : Checking Pending Approval Requests**
  

  Checks the status of pending approval requests -- goes to Smart Contract 5, queries Smart Contract 3, and checks against Smart Contract 4 to see if a request has *already* been approved
  
	input: approval_user_id
	output: list of [filename, requestor] pairs

  **API 5 : Getting encrypted_secret_shares_with_approver_public_key**
  

  Gets the encrypted secret shares shared with a requestor. 
  
	input: p2pFileName, approver_userid
	output: encrypted_secret_shares_with_approver_public_key
	
  **API 6 : Approving Requests**
  

  Approves a request for access of a patient  file. 
  
	input: p2pFileName, approver_userid, requester_userid, encrypted_secret_shares_encrypted_with_requestor_public_key
	output: status message
	
  **API 7 : User Public Key Creation**
  

  Creates a public key to associate with a given user id. 
  
	input: user_id, public_key
	output: status message


  **API 8 : Getting User Associated File Names**
  
  
  Gets a list of filenames associated with the user. 
  
	input: Ethereum address
	output: A list of p2pFilenames


  **API 9 : Getting Ethereum Addresses**
  

  Gets the Ethereum Block Chain address for a patient 

	input: (Username, Birthday)
	output: Ethereum Address


  **API 10: Creating a Patient's Ethereum Address**
  

  Links and creates an Ethereum Block Chain address to a patient's username and birthday.

	input: (Username, Birthday)
	output:  Ethereum Address
	
  **API 11 : Request Authorization** 


  Creates an authorization for a patient file 
  
  	input : (requester_userid, p2pFileName)
	output : p2p file request

  **API 12 : Adding Files to a User (OVERLAPPING WITH 1)** 

  
  Add a file to the associated user i.e. patient in Ethereum/HealthShare. 
  
	input: Ethereum address, file_name
	output: n/a 

  **API 13 : Deleting a File from a User** 


  Deletes a file associated with a user/patient in Ethereum/HealthShare. 
  
	input:  Ethereum address
	output: n/a

  **API 14 : Getting a List of Files with Secret Shares** 

  
  Gets a list of files for a user which were approved by another. 
  
	input: Ethereum address
	output: A list of p2pFilenames with encrypted secret share

  **Verification and Testing**

  To verify that the APIs are all functioning correctly between the web
  front-end and multiple backend Block Chains, consider running test/test.py. 

### III. Access Granting Example <a name="use_case_example"></a>
---
To better illustrate and show the design of HealthShare, let us examine the following scenario. Say that we have our patient, Tony, who has authorized his friends Elgin and Harrison as secret share holders. Our system will represent Tony as the following...
#### i. System Setup 

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
 
 #### ii. Quang's Request
Quang, a 3rd party, wants and requests for access to Tony's file. To gain access, Quang needs any of the two shares in [123,456,789]. The system logs Quang's request and sends notifications to the share owners : Tony, Elgin, and Harrison asking them if they will both approve and grant Quang's access.

 #### iii. Approving Share Owners
 
  **1) Elgin approves of Quang** 
  
   - Elgin fetches his own secret share, encrypted_secret_share_Elgin, from *Smart Contract 2*
   - Decrypts his own secret share to get [123] and 
   - Then he re-encrypts [123] under Quang's public key to get encrypted_secret_shares_encrypted_Quang and stores the result in this in 	*Smart Contract 4*

  **2) Tony also approves of Quang**
  
   - Tony fetches also fetches his own share, encrypted_secret_share_Tony, from *Smart Contract 2*
   - Decrypts encrypted_secret_share_Tony to get [456] and 
   - Then re-encrypts [456] under Quang's public key to get encrypted_secret_shares_encrypted_Quang and similarly, stores the result in *Smart Contract 4*
  
  At this point, 2 of out of the 3 share owners have approved of Quang granting him access to Tony's file. It is no longer necessary for Harrison to approve of Quang. However, he can still approve of Quang if he desires to choose so, but as far as Quang is concerned, he now has access to Tony's file which is all that matters to him.

#### iv. Quang gets Access
Once Tony and Elgin have approved and sent their secret shares to Quang, Quang sees <Tony, encrypted_secret_shares_encrypted_Quang> and <Elgin, encrypted_secret_shares_encrypted_Quang>. Using his secret key, he is able to decrypt both and receive [123] and [456] from Tony and Elgin respectively. Now holding the required 2 out of 3 shares, Quang is able to recreate and use the secret key, 123456789, to gain access to Tony's file. 
