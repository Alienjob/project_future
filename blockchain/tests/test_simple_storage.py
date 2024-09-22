import pytest
from brownie import SimpleStorage, accounts

def test_deploy():
    # Arrange
    account = accounts[0]
    
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    
    # Assert
    assert simple_storage.get() == 0

def test_updating_storage():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    
    # Act
    expected = 15
    simple_storage.set(expected, {"from": account})  # Changed from store to set
    
    # Assert
    assert simple_storage.get() == expected