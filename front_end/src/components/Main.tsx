/* eslint-disable spaced-comment */
/// <reference types="react-scripts"/> // for importing pngs

import { useEthers } from "@usedapp/core"
import helperConfig from "../helper-config.json"
import networkMapping from "../chain-info/deployments/map.json"
import { constants, ethers } from "ethers"
import brownieConfig from "../brownie-config.json"
import dapp from "../dapp.png"
import eth from "../eth.png"
import dai from "../dai.png"
import { YourWallet } from "./yourWallet"

export type Token = {
    image: string
    address: string
    name: string
}

export const Main = () => {
    //Show token values from the wallet

    //Get tge address of different tokens
    //Get the balance of the users wallet

    //send the brownie-cfg to ou 'src' folder
    //send the build folder
    let nrStr = "1337"
    const { chainId, error } = useEthers()
    if (chainId !== undefined) {
        nrStr = chainId.toString()
    }
    const networkName = chainId ? helperConfig[nrStr] : "dev"
    console.log(networkName)

    const dappTokenAddress = chainId ? networkMapping[String(chainId)]["DappToken"][0] : constants.AddressZero
    const wethTokenAddress = chainId ? brownieConfig["networks"][networkName]["weth"] : constants.AddressZero
    const fauTokenAddress = chainId ? brownieConfig["networks"][networkName]["fau"] : constants.AddressZero

    const supportedTokens: Array<Token> = [
        {
            image: dapp,
            address: dappTokenAddress,
            name: "DAPP"
        },
        {
            image: eth,
            address: wethTokenAddress,
            name: "WETH"
        },
        {
            image: dai,
            address: fauTokenAddress,
            name: "DAI"
        }
    ]


    return (<YourWallet supportedTokens={supportedTokens} />)
}