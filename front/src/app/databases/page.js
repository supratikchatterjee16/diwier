"use client";

import { useState, useEffect } from "react";
import { ThemeProvider, CssBaseline, Container } from "@mui/material";
import { lightTheme, darkTheme } from "../commons/theme";

import Toolbar from "../components/Toolbar";

import { ConnectionsList, EnvironmentList } from "../components/lists";

export default function DatabasesPage() {
  let [envs, setEnvs] = useState([]);
  const onEnvChange = (e) => {
    setEnvs(e);
  };
  let [theme, setTheme] = useState(lightTheme);
  useEffect(() => {
    if (window.matchMedia("(prefers-color-scheme: dark)")) 
      setTheme(darkTheme);
  });
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Toolbar select="databases" />
      <Container maxWidth="xl" sx={{ paddingTop: "20pt" }}>
        <EnvironmentList onEnvChange={onEnvChange} />
        <ConnectionsList envs={envs} />
      </Container>
    </ThemeProvider>
  );
}
