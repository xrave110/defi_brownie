import React from 'react';
import { DAppProvider, Kovan } from "@usedapp/core"
import { Header } from "./components/Header"
import { Container } from "@material-ui/core"
import { Main } from "./components/Main"


function App() {
  return (
    <DAppProvider config={{
      networks: [Kovan],
      notifications: {
        expirationPeriod: 1000,
        checkInterval: 100,
      },
    }}>
      <Header />
      <Container maxWidth="sm">
        <div>Hi!</div>
        <Main />
      </Container>
    </DAppProvider>
  )
}

export default App;
