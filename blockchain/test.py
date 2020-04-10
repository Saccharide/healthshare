import requests

"""
test.py is a set of basic API tests to make sure that the various components of
HealthShare are operating correctly. It is up to the user to ensure that the
various settings and configuration data is managed properly to run on their system.
"""

BASE_URL = "http://localhost:3000"
ACCOUNT_0 = "0x06f47c9896f0e953af35320d61f020e8401002bc"
ACCOUNT_1 = "0x7818c1e4713b6c45d0fd45cdba76089dbe37152d"

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
assert 'file1' in [a["filename"] for a in res.json()["data"]]

# API 6: APPROVE a file access request
res = requests.post("{}/approve".format(BASE_URL), json={
    "filename": "file1",
    "requestor": ACCOUNT_0,
    "encrypted_share": "SECRET_SHARE1",
    "user_id": ACCOUNT_1
})
assert res.json()["data"]

# API 14: GET approved list secrets
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

print("Starting functionality testing")
print("Function 1: creating user")
username = 'Elgin'
password = 'password'
private_key = '''-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAsmvCJucgwzymasVYK95VUt1zMcD/TtsyWCCjfO0JK1vd1edN
ipHBWDDiFND0IH0GY0CGeJYX4uzf8/VPfchsN/Qrn9U/l5smE9DGGbM+pwBHQvpc
qac2YPQAY9s2t6xVF5PfAUZMvfDNJqA+coJufL2YxsTk0QgAcpfAkTLscM5KF3YN
6MCOb4ElWeZLqmRuSKW8kywFw3tNctwlkUzgu/KqRRfdyfzZEsWgKZkzGrqHDOaV
wWwSqWL66p/OFgxw1fxSycJSQQwkikyaF/PVYpZc00tKudw2nS5Tn4W+g7TvBzWu
meZ4wDK4Ik8uIc0Bfxzw6bNVAda5iy2DfNwe5QIDAQABAoIBAEv4SB4Kcc/PxkhW
KPnc3FXBRyhbNhpciO4vT42E3E+i+Sz4JPMoprunbMxSQHCI66xdMCSuPBN6qs0U
mblEGpgklmKjCUXDYQ406fTNdpLjMnSZZ9UxBp13p6bdE0pXzY+RffXr+gcyPhgB
STW2xdbFYATal1dN4erpJKxuk3BgH9wy/aqo9d9Ft0+qzYHDt1Kf1JhrhOgA2KnP
Ndu+vdOYStglLLGaDUoNolTk/IQF43Q7PyYmzcRjqSQbxWYohPX98yYVjCO7/BHq
hLrgXIQPDFziN5mnmAX6IVQy2Ft0wuhriAvLuGA/5twwfxA1iLxAzreKWYhTkei2
CNHSiuECgYEA3XhQ34bnuOrqk1KJHCYyHJhP7/mpBc3hlLhPkvczkGQzbhy6UEix
cF1k2fuJ8jS+epVrqVMKWt3WOJaFAd2tgAOOkbFaFc18WDpbeN2uvA/IrzRprFwL
0MGGLM7hZDR+uZU80ZjW9VBivVx1wQbthfx1AtoW9K+cVUV7nKiFnckCgYEAzj0y
LDrClQ8zn6hk1colaRapDRTPGq2rZyXLTFkWJxpFZCuq+47m5APaXNIwOu9pZfCB
j+FgxhYfCIxemRXGygLnpc/FNmAqsYQXMiZl8oXXoMvIW7NG8Bh16X47AxI9iRLV
eZeEHPkLIeYoJVSXF1BntAE8DtTpGU8d/BPkVj0CgYEAm6XSWLYsJtba030fJWxm
rZgSHhq9QnoGPwolyqj3UVRKnOmNu5zLL6hDl7tjoJiXAfn/dzoIPgJIau7GPaB5
Lk3Rpe0Z3dbTvAIPhWtvQXZqWVAhsGPkXeuUi+s9lroaEf2jh7693ByJuIHBtE5V
ImRiLAXwOjktSvSRQnFhrpkCgYAMXG6daAgxlu+pKhahGbSUT99iAVVIbBBR5loB
AXXqchCmqFdfLHl6QSDdX1u0rJTMn1WkogWC2eCSSpeA5WU8xl/L+GABmlH0wc4C
G3sQxiTeZlhj5qLh0RWAISi4TmeRx6cz2nj4o5SfO4Q8eI11wEP27fwDh49RDQTn
DuoooQKBgQC1srKHHwB/nnoDmbS4V4LgXJ1GKBxQo6s/Yu07z6TJYMPOKd5SrwMe
4G35aULYhrSH+HZ1Tjv4PphJdSCH5wz/HbVVvSRrJXOaR0rx4q93hn2JpWCZqjed
T15PeJG5GBNoACDlFyc20q3tx/jHFczhaU4l4buNJ+zO/5AJrSDWPQ==
-----END RSA PRIVATE KEY-----'''
public_key = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsmvCJucgwzymasVYK95V
Ut1zMcD/TtsyWCCjfO0JK1vd1edNipHBWDDiFND0IH0GY0CGeJYX4uzf8/VPfchs
N/Qrn9U/l5smE9DGGbM+pwBHQvpcqac2YPQAY9s2t6xVF5PfAUZMvfDNJqA+coJu
fL2YxsTk0QgAcpfAkTLscM5KF3YN6MCOb4ElWeZLqmRuSKW8kywFw3tNctwlkUzg
u/KqRRfdyfzZEsWgKZkzGrqHDOaVwWwSqWL66p/OFgxw1fxSycJSQQwkikyaF/PV
YpZc00tKudw2nS5Tn4W+g7TvBzWumeZ4wDK4Ik8uIc0Bfxzw6bNVAda5iy2DfNwe
5QIDAQAB
-----END PUBLIC KEY-----'''
name = "Elgin"
birthdate = "24/11/1994"

# Create ETH address
# TO BE DONE, for not take the account ID as ACCOUNT_0

# associate public key
print("Associating Public Key:")
res = requests.post("{}/setPublicKey".format(BASE_URL), json={
    "user_id": ACCOUNT_0,
    "public_key": public_key
})
print(res.json()['data'])


print("Function 2: Uploading a File")
FILENAME = 'file1'
# Upload File
res = requests.post("{}/addFile".format(BASE_URL), json={
    "user_id": ACCOUNT_0,
    "file_name": FILENAME
})
print(res.json()['data'])

# Set Approver of File
res = requests.get("{}/getAddressFromDetails?name={}&birthday={}".format(BASE_URL, "Alice", "02/29/2020"))
print(res.json()['data'])

approver_address = res.json()['data']

res = requests.post("{}/setApprover".format(BASE_URL), json={
    "filename": FILENAME,
    "approver_id": approver_address,
    "encrypted_secret_share": "ENCRYPTED_SECRET_SHARE1",
    "user_id": ACCOUNT_0
})

print(res.json()['data'])
