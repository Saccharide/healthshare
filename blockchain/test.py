import requests

BASE_URL = "http://localhost:3000"
ACCOUNT_0 = "0x6ad49E1a1243a3B8629E47bD603c8bbc684D1147"

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


print("All testcases passed")
