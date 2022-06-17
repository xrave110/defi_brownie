import { Token } from "../Main"
import React, { useState } from "react"
import { Box } from "@material-ui/core"
import { Tabs } from "@material-ui/core"
import { Tab } from "@material-ui/core"



interface YourWalletProps {
    supportedTokens: Array<Token>
}

export const YourWallet = ({ supportedTokens }: YourWalletProps) => {
    const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0)
    return (
        <Box>
            <h1>
                Your Wallet
            </h1>
            <Box>
                <Tabs value={selectedTokenIndex} onChange={handleChange} aria-label="basic tabs example">
                    <Tab label="Item One" {...a11yProps(0)} />
                    <Tab label="Item Two" {...a11yProps(1)} />
                    <Tab label="Item Three" {...a11yProps(2)} />
                </Tabs>
                {/* {supportedTokens.map((token, index) => {
                            <Tab label={token.name}
                                value={index.toString()}
                                key={index} />
                        })} */}

            </Box>
        </Box >
    )
}