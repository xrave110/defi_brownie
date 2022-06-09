from brownie import network, exceptions, interface
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
    INITIAL_PRICE_FEED_VALUE,
)
from scripts.deploy import deploy_token_farm_and_dapp_token
from conftest import *
import pytest


def test_set_price_feed_contract():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    account = get_account()
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    price_feed_address = get_contract("eth_usd_price_feed")
    # Act
    token_farm.setPriceFeedContract(
        dapp_token.address, price_feed_address, {"from": account}
    )
    # Assert
    assert token_farm.tokenPriceFeedMapping(dapp_token.address) == price_feed_address
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedContract(
            dapp_token.address, price_feed_address, {"from": non_owner}
        )


def test_stake_tokens(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    account = get_account()
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # Act
    dapp_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, dapp_token.address, {"from": account})
    # Assert
    assert (
        token_farm.stakingBalance(dapp_token.address, account.address) == amount_staked
    )
    assert token_farm.uniqueTokenStaked(account.address) == 1
    assert token_farm.stakers(0) == account.address
    return token_farm, dapp_token


def test_token_is_allowed():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    account = get_account()
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()

    list_of_allowed_tokens = [token_farm.allowedTokens(x) for x in range(3)]
    print((list_of_allowed_tokens))
    # Act/Assert
    allowed = token_farm.tokenIsAllowed(dapp_token.address)
    assert allowed == True

    allowed = token_farm.tokenIsAllowed("0x6951b5Bd815043E3F842c1b026b0Fa888Cc2DD45")
    assert allowed == False


def test_get_single_token_value(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    account = get_account()
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # Act
    dapp_token.approve(token_farm.address, amount_staked, {"from": account})
    print(token_farm.tokenIsAllowed(token_farm.address))
    token_farm.stakeTokens(amount_staked, dapp_token.address, {"from": account})
    dapp_token_value = token_farm.getUserSingleTokenValue(
        account.address, dapp_token.address
    )
    expected_value = (
        token_farm.stakingBalance(dapp_token.address, account.address)
        * (INITIAL_PRICE_FEED_VALUE)
    ) / (10 ** dapp_token.decimals())
    assert dapp_token_value == expected_value


def test_user_total_value(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    account = get_account()
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # Act
    with pytest.raises(exceptions.VirtualMachineError):
        print(token_farm.getUserTotalValue(account.address))
    dapp_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, dapp_token.address, {"from": account})
    list_of_allowed_tokens = [token_farm.allowedTokens(x) for x in range(3)]

    print(token_farm.getUserSingleTokenValue(account.address, dapp_token.address))
    print(
        token_farm.getUserSingleTokenValue(account.address, list_of_allowed_tokens[1])
    )
    print(token_farm.getUserSingleTokenValue(account, list_of_allowed_tokens[2]))

    # Arrange
    total_value_1 = token_farm.getUserTotalValue(account.address)
    print(token_farm.getUserTotalValue(account.address))
    expected_value = (
        token_farm.stakingBalance(dapp_token.address, account.address)
        * (INITIAL_PRICE_FEED_VALUE)
    ) / (10 ** dapp_token.decimals())
    assert total_value_1 == expected_value
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.stakeTokens(
            amount_staked, list_of_allowed_tokens[2], {"from": account}
        )
    weth_token = get_contract("weth")
    # weth_token._mint(account, 1.1 * amount_staked)

    weth_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, weth_token.address, {"from": account})
    print(
        "Weth: {}".format(
            token_farm.stakingBalance(weth_token.address, account.address)
        )
    )
    print(
        "Dapp: {}".format(
            token_farm.stakingBalance(dapp_token.address, account.address)
        )
    )
    print("Expected 1: {}".format(expected_value))
    expected_value += (
        token_farm.stakingBalance(weth_token.address, account.address)
        * (INITIAL_PRICE_FEED_VALUE)
    ) / (10 ** dapp_token.decimals())
    print("Expected 2: {}".format(expected_value))
    total_value_2 = token_farm.getUserTotalValue(account.address)
    assert total_value_2 == expected_value


def test_issue_tokens(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    account = get_account()
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    starting_balance = dapp_token.balanceOf(account.address)
    weth_token = get_contract("weth")

    # Act
    token_farm.issueTokens({"from": account})

    # Assert
    assert dapp_token.balanceOf(account.address) == starting_balance

    weth_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, weth_token.address, {"from": account})
    token_farm.issueTokens({"from": account})

    assert dapp_token.balanceOf(account.address) == (
        starting_balance
        + (
            token_farm.stakingBalance(weth_token.address, account.address)
            * (INITIAL_PRICE_FEED_VALUE)
        )
        / (10 ** dapp_token.decimals())
    )
