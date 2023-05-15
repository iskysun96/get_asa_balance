from beaker import *
from pyteal import *

app = Application("Get Asset Balance")


@app.external
def asa_balance_with_reference_type(
    account: abi.Account, asa: abi.Asset, *, output: abi.Uint64
) -> Expr:
    asset_balance = AssetHolding.balance(account.address(), asa.asset_id())
    return Seq(
        asset_balance,
        If(asset_balance.hasValue())
        .Then(output.set(asset_balance.value()))
        .Else(Reject()),
    )


@app.external
def asa_balance_with_slot_referencing(*, output: abi.Uint64) -> Expr:
    asset_balance = AssetHolding.balance(Txn.accounts[0], Txn.assets[0])
    return Seq(
        asset_balance,
        If(asset_balance.hasValue())
        .Then(output.set(asset_balance.value()))
        .Else(Reject()),
    )


if __name__ == "__main__":
    app.build().export("./artifacts")
