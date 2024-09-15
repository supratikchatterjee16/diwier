"use client";

import {useState } from "react";
import { Container } from "@mui/material";

import Toolbar from "../components/Toolbar";

import { ConnectionsList, EnvironmentList } from "../components/lists";

export default function DatabasesPage() {
  let [envs, setEnvs] = useState([]);
  const onEnvChange = (e) => {setEnvs(e);};
  return (
    <>
      <Toolbar select="databases" />
      <Container maxWidth="xl" sx={{ paddingTop: "20pt" }}>
        <EnvironmentList onEnvChange={onEnvChange}/>
        <ConnectionsList envs={envs}/>
      </Container>
    </>
  );
}
