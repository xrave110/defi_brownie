from scripts.helpful_scripts import get_account, get_contract
from brownie import DappToken, TokenFarm, config, network
from web3 import Web3

KEPT_BALANCE = Web3.toWei(100, "ether")


def deploy_token_farm_and_dapp_token():
    account = get_account()
    dapp_token = DappToken.deploy({"from": account})
    token_farm = TokenFarm.deploy(
        dapp_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    tx = dapp_token.transfer(
        token_farm.address, dapp_token.totalSupply() - KEPT_BALANCE, {"from": account}
    )
    tx.wait(1)
    # dapp_token, weth_token, fau_token/dai
    weth_token = get_contract("weth")
    fau_token = get_contract("fau")

    dict_of_allowed_tokens = {
        dapp_token.address: get_contract("dai_usd_price_feed"),
        fau_token.address: get_contract("dai_usd_price_feed"),
        weth_token.address: get_contract("eth_usd_price_feed"),
    }
    add_allowed_tokens(token_farm, dict_of_allowed_tokens, account)
    return token_farm, dapp_token


def add_allowed_tokens(token_farm, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        add_tx = token_farm.addAllowedTokens(token, {"from": account})
        add_tx.wait(1)
        send_tx = token_farm.setPriceFeedContract(
            token, dict_of_allowed_tokens[token], {"from": account}
        )
        # print(dict_of_allowed_tokens)
        send_tx.wait(1)


def main():
    deploy_token_farm_and_dapp_token()