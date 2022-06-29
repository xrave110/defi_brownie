import { useEthers, useTokenBalance } from "@usedapp/core"
import { Token } from "../Main"


export interface WalletBalanceProps {
    token: Token
}

export const WalletBalance = ({ token }: WalletBalanceProps) => {
    const { image, address, name } = token
    const { account } = useEthers()
    const tokenBalance = useTokenBalance(address, account)
    console.log("Here I am" + tokenBalance?.toString())
    return (<div>I'm the wallet balance!</div>)
}