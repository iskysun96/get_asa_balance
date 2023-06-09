import json
from algosdk.transaction import *
from beaker import sandbox

# Initialize an algod client
algod_client = sandbox.get_algod_client()

accounts = sandbox.kmd.get_accounts()
sender = accounts[0]

sk = sender.private_key
pk = sender.address

# CREATE ASSET
# Get network params for transactions before every transaction.
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
# params.fee = 1000
# params.flat_fee = True
# Account 1 creates an asset called latinum and
# sets Account 2 as the manager, reserve, freeze, and clawback address.
# Asset Creation transaction
txn = AssetConfigTxn(
    sender=pk,
    sp=params,
    total=1000,
    default_frozen=False,
    unit_name="APPL",
    asset_name="Apple",
    manager=pk,
    reserve=pk,
    freeze=pk,
    clawback=pk,
    url="https://path/to/my/asset/details",
    decimals=0,
)
# Sign with secret key of creator
stxn = txn.sign(sk)
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))
except Exception as err:
    print(err)
# Retrieve the asset ID of the newly created asset by first
# ensuring that the creation transaction was confirmed,
# then grabbing the asset id from the transaction.
print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))
