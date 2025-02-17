import requests

"""
test.py is a set of basic API tests to make sure that the various components of
HealthShare are operating correctly. It is up to the user to ensure that the
various settings and configuration data is managed properly to run on their system.
"""

BASE_URL = "http://localhost:3000"
ACCOUNT_0 = "0xc69f09325d43e67785bf517211794794e0747c61"
ACCOUNT_1 = "0x1e734adb5198006d7c9b1644f45c8f5991f64346"

# API 7: SET public key
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

# API 2: GET public key
res = requests.get("{}/getPublicKey?user_id={}".format(BASE_URL, ACCOUNT_0))
# {
#     "data": "MYPUBKEY"
# }
assert res.json()["data"] == "MYPUBKEY"

# API 1: ASSOCIATE a file with a user
res = requests.post("{}/addFile".format(BASE_URL), json={
    "user_id": ACCOUNT_0,
    "file_name": "file1"
})
# SAMPLE RESPONSE: see API 7
assert res.json()["data"]

# API 8: GET files associated with a user
res = requests.get("{}/getFiles?user_id={}".format(BASE_URL, ACCOUNT_0))
assert "file1" in res.json()["data"]

# API 10: SET name and birthday to an address
res = requests.post("{}/setDetails".format(BASE_URL), json={
    "name": "Alice",
    "birthday": "02/29/2020",
    "user_id": ACCOUNT_1
})
assert res.json()["data"]

# API 9: GET address from name and birthday
res = requests.get("{}/getAddressFromDetails?name={}&birthday={}".format(BASE_URL, "Alice", "02/29/2020"))
assert res.json()["data"].lower() == ACCOUNT_1.lower()


# API 3: SET approver_id of file
res = requests.post("{}/setApprover".format(BASE_URL), json={
    "filename": "file1",
    "approver_id": ACCOUNT_1,
    "encrypted_secret_share": "ENCRYPTED_SECRET_SHARE1",
    "user_id": ACCOUNT_0
})
assert res.json()["data"]

# API 5: GET approver secret
res = requests.get("{}/getApproverSecret?filename={}&approver_id={}".format(BASE_URL, "file1", ACCOUNT_1))
assert res.json()["data"] == "ENCRYPTED_SECRET_SHARE1"

# API 11: REQUEST to access a file
res = requests.post("{}/requestFile".format(BASE_URL), json={
    "filename": "file1",
    "user_id": ACCOUNT_0
})
assert res.json()["data"]

# API 4: GET approval request list
res = requests.get("{}/getApprovableList?user_id={}".format(BASE_URL, ACCOUNT_1))
assert 'file1' in res.json()["data"]

# API 6: APPROVE a file access request
res = requests.post("{}/approve".format(BASE_URL), json={
    "filename": "file1",
    "requestor": ACCOUNT_0,
    "encrypted_share": "SECRET_SHARE1",
    "user_id": ACCOUNT_1
})
assert res.json()["data"]

<<<<<<< HEAD
# API 12: GET approver list
=======
# API 14: GET approved list secrets
>>>>>>> 49431489d4db3bd173581fc907e406c9b2f86c6c
res = requests.get("{}/getApprovedListSecrets?user_id={}".format(BASE_URL, ACCOUNT_0))
assert [d
        for d in res.json()["data"]
        if d["filename"] == "file1" and d["secret_share"] == "SECRET_SHARE1"
        ]

# API 13: Remove a file
res = requests.post("{}/removeFile".format(BASE_URL), json={
    "filename": "file1",
    "user_id": ACCOUNT_0
})
assert res.json()["data"]

print("All testcases passed")
