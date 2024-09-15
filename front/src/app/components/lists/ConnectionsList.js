"use client";

import { useEffect, useState } from "react";
import {
  Accordion,
  AccordionActions,
  AccordionDetails,
  AccordionSummary,
  Box,
  Button,
} from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";

import { connService } from "@/app/services/connectionService";

import { AddConnDialog, ModifyConnDialog } from "@/app/dialogs";

export default function ConnectionsList({ envs, controls = true }) {
  const conCols = [
    { field: "name", headerName: "Name", width: 150 },
    { field: "env_name", headerName: "Environment Name", width: 250 },
    { field: "provider", headerName: "Provider", width: 150 },
    { field: "ip", headerName: "IP", width: 250 },
    { field: "schema", headerName: "Schema", width: 100 },
  ];

  const [openConnAdd, setOpenConnAdd] = useState(false);
  const [openConnModify, setOpenConnModify] = useState(false);
  const [selectedConns, setSelectedConns] = useState([]);
  const [connDel, setConnDel] = useState(true);
  const [connMod, setConnMod] = useState(true);
  const [connRows, setConnRows] = useState([]);
  const connActions = {
    fetch: async () => {
      const conns = await connService.get();
      console.log(conns);
      let id = 0;
      setConRows(
        conns.data.map((conn) => {
          return { ...conn, id: id++ };
        })
      );
    },
    add: async () => {
      const resp = await envService.post({
        name: document.getElementById("conn-name").value,
        env_name: document.getElementById("conn-env-name").value,
        provider: document.getElementById("conn-provider").value,
        ip: document.getElementById("conn-ip").value,
        schema: document.getElementById("conn-schema").value,
        user: document.getElementById("conn-user").value,
        psk: document.getElementById("conn-psk").value,
      });
      if (resp.status == 200) {
        setConnRows((envRows) => [
          ...envRows,
          { ...resp.data, id: envRows[envRows.length - 1].id + 1 },
        ]);
        envActions.closeAddPrompt();
      }
    },
    update: async () => {},
    delete: async () => {
      const conns = selectedConns.map((val) => {
        return { name: connRows[val].name, desc: connRows[val].desc };
      });
      const resp = await connService.delete({ data: conns });
      if (resp.status == 200) {
        connActions.fetch();
        setConnDel(true);
      }
    },
    select: (newSelection) => {
      if (newSelection.length > 0) {
        setConnDel(false);
        if (newSelection.length == 1) setConnMod(false);
        else setConnMod(true);
      } else {
        setConnDel(true);
        setConnMod(true);
      }
      setSelectedConns(newSelection);
    },
    openAddPrompt: () => {
      setOpenConnAdd(true);
    },
    closeAddPrompt: () => {
      setOpenConnAdd(false);
    },
    openModifyPrompt: () => {
      setOpenConnModify(true);
    },
    closeModifyPrompt: () => {
      setOpenConnModify(false);
    },
  };

  useEffect(() => {
    connService.initialize();
    connActions.fetch();
  });

  let actions = (
      <AccordionActions>
        <Button onClick={connActions.openAddPrompt}>Add</Button>
        <Button onClick={connActions.openModifyPrompt} disabled={connMod}>
          Modify
        </Button>
        <Button onClick={connActions.delete} disabled={connDel}>
          Delete
        </Button>
      </AccordionActions>
    ),
    dialogs = (
      <>
        <AddConnDialog
          open={openConnAdd}
          closeAction={connActions.closeAddPrompt}
          addAction={connActions.add}
          environments={envs}
        />
        <ModifyConnDialog
          open={openConnModify}
          closeAction={connActions.closeModifyPrompt}
          modifyAction={connActions.update}
          environments={envs}
        />
      </>
    );
    if(!controls){
        actions = null;
        dialogs = null;
    }
  return (
    <>
      <Accordion defaultExpanded>
        <AccordionSummary>Connections</AccordionSummary>
        <AccordionDetails>
          <Box sx={{ height: 500, width: "100%" }}>
            <DataGrid
              rows={connRows}
              columns={conCols}
              initialState={{
                pagination: {
                  paginationModel: { page: 0, pageSize: 50 },
                },
              }}
              pageSizeOptions={[5, 10, 50, 100]}
              checkboxSelection
              onRowSelectionModelChange={connActions.select}
            />
          </Box>
        </AccordionDetails>
        {actions}
      </Accordion>
      {dialogs}
    </>
  );
}
