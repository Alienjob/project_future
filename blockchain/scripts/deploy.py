from brownie import SimpleStorage, accounts

def main():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    print(f"Contract deployed to: {simple_storage.address}")
    return simple_storage