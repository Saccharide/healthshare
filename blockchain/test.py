import requests

"""
test.py is a set of basic API tests to make sure that the various components of 
HealthShare are operating correctly. It is up to the user to ensure that the
various settings and configuration data is managed properly to run on their system. 
"""

BASE_URL = "http://localhost:3000"
ACCOUNT_0 = "0x6ad49e1a1243a3b8629e47bd603c8bbc684d1147"
ACCOUNT_1 = "0xb38a6b63ce227fab60f33b6237bfe7934301741b"

# API 7: SET PUBLIC KEY
res = requests.post("{}/setPublicKey".format(BASE_URL), json={
    "user_id": ACCOUNT_0,
    "public_key": "MYPUBKEY"
})
# {
#     "data": {
#         "tx": "0x8a97f3a50f8694196798e818e01761a8dc7b665d1c43f0e8afc1748e3a7107ca",
#         "receipt": {
#             "transactionHash": "0x8a97f3a50f8694196798e818e01761a8dc7b665d1c43f0e8afc1748e3a7107ca",
#             "transactionIndex": 0,
#             "blockHash": "0xd2abcb011888916796f74ceb548ba74e62d3b61c1d7759f7045054f1ddc7e190",
#             "blockNumber": 57,
#             "from": "0xde6bc281b6d3844c60a38e6f5ed1ee8729929492",
#             "to": "0x2be3e7e5c4e46eda403d95d71346c58b5116df55",
#             "gasUsed": 33548,
#             "cumulativeGasUsed": 33548,
#             "contractAddress": null,
#             "logs": [
#
#             ],
#             "status": true,
#             "logsBloom": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
#             "v": "0x1c",
#             "r": "0xcbdee6fbdea0bf3aed2d87e6e9e4489fd7008f126258c10ff808536cae1aaf95",
#             "s": "0x459bcf3398f52202f8ebaed9de141b63488ef472d5a31e82412f5c2c2a92ef5c",
#             "rawLogs": [
#
#             ]
#         },
#         "logs": [
#
#         ]
#     }
# }
assert res.json()["data"]

# API 2: GET PUBLIC KEY
res = requests.get("{}/getPublicKey?user_id={}".format(BASE_URL, ACCOUNT_0))
# {
#     "data": "MYPUBKEY"
# }
assert res.json()["data"] == "MYPUBKEY"

# API 8: ASSOCIATE A FILE WITH A USER
res = requests.post("{}/addFile".format(BASE_URL), json={
    "user_id": ACCOUNT_0,
    "file_name": "file1"
})
# SAMPLE RESPONSE: see API 7
assert res.json()["data"]

# API 1: GET FILES OF USERS
res = requests.get("{}/getFiles?user_id={}".format(BASE_URL, ACCOUNT_0))
assert "file1" in res.json()["data"]

# API 10: SET name and birthday
res = requests.post("{}/setDetails".format(BASE_URL), json={
    "name": "Alice",
    "birthday": "02/29/2020",
    "user_id": ACCOUNT_1
})
assert res.json()["data"]

# API 9: GET name and birthday
res = requests.get("{}/getAddressFromDetails?name={}&birthday={}&user_id={}".format(BASE_URL, "Alice", "02/29/2020", ACCOUNT_0))
assert res.json()["data"].lower() == ACCOUNT_1.lower()


# API 3: SET approver_id
res = requests.post("{}/setApprover".format(BASE_URL), json={
    "filename": "file1",
    "approver_id": ACCOUNT_1,
    "encrypted_secret_share": "SECRET_SHARE1",
    "user_id": ACCOUNT_0
})
assert res.json()["data"]

# API 5: GET approver secret
res = requests.get("{}/getApproverSecret?filename={}&approver_id={}".format(BASE_URL, "file1", ACCOUNT_1))
assert res.json()["data"] == "SECRET_SHARE1"

print("All testcases passed")
