from app import app, asa_balance_with_reference_type, asa_balance_with_slot_referencing
from beaker import sandbox, client

app.build().export("./artifacts")

accounts = sandbox.kmd.get_accounts()
sender = accounts[0]

app_client = client.ApplicationClient(
    client=sandbox.get_algod_client(),
    app=app,
    sender=sender.address,
    signer=sender.signer,
)

app_client.create()


# Get ASA balance with reference types
return_value = app_client.call(
    asa_balance_with_reference_type, account=sender.address, asa=265
).return_value
print(return_value)

# Get ASA balance with slot referencing
return_value2 = app_client.call(
    asa_balance_with_slot_referencing, accounts=[sender.address], foreign_assets=[265]
).return_value

print(return_value2)
