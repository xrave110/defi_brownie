import { useEthers, useContractFunction } from "@usedapp/core"
import { constants, utils } from "ethers"
import { Contract } from "@ethersproject/contracts"
import TokenFarm from "../chain-info/contracts/TokenFarm.json"
import ERC20 from "../chain-info/contracts/DappToken.json"
import networkMapping from "../chain-info/deployments/map.json"
import { useEffect, useState } from 'react'


export const useStakeToken = (tokenAddress: string) => {
    //address
    //abi
    //chainId
    const { chainId } = useEthers()
    const { abi } = TokenFarm
    const tokenFarmAddress = chainId ? networkMapping[String(chainId)]["TokenFarm"][0] : constants.AddressZero
    const tokenFarmInterface = new utils.Interface(abi)
    const tokenFarmContract = new Contract(tokenFarmAddress, tokenFarmInterface)
    //approve
    const erc20Abi = ERC20.abi
    const erc20Interface = new utils.Interface(erc20Abi)
    const erc20Contract = new Contract(tokenAddress, erc20Interface)
    const { send: approveErc20Send, state: approveErc20State } = useContractFunction(erc20Contract, "approve",
        { transactionName: "Approve ERC20 transfer" })
    const approveAndStake = (amount: string) => {
        setAmountToStake(amount)
        return approveErc20Send(tokenFarmAddress, amount)
    }

    const { send: stakeSend, state: stakeState } = useContractFunction(tokenFarmContract, "stake",
        { transactionName: "stakeTokens" })


    const [amountToStake, setAmountToStake] = useState("0")
    //triggered by approveErc20State 
    useEffect(() => {
        if (approveErc20State.status === "Success") {
            //state
            stakeSend()
        }
    }, [approveErc20State])

    //const [state, setState] = useState(approveErc20State)
    return { approveAndStake, approveErc20State }
}