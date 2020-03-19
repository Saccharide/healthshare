(18/03/2020) Things to do:
1) Blockchain logging (T and Q)
2) Blockchain retrival of filename (T and Q)
3) Blockchain updating of records (T and Q)
4) Blockchain query interface (T and Q)
5) Crypto Wrapper for DHT (E)
6) Web application (Integration) (E)
7) Documentation and presentation (H)

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
