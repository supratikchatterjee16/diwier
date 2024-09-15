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

import { AddEnvDialog } from "@/app/dialogs";
import { envService } from "@/app/services/environmentService";

/**
 * EnvironmentList component that accepts a state variable
 * and function for managing Environment State in parent component.
 *
 * @returns A list with some action buttons and dialogue
 */
export default function EnvironmentList({ onEnvChange, controls = true }) {
  const envCols = [
    { field: "name", headerName: "Name", width: 200 },
    { field: "desc", headerName: "Description", width: 500 },
  ];
  const [openEnvAdd, setOpenEnvAdd] = useState(false);
  const [selectedEnvs, setSelectedEnvs] = useState([]);
  const [envDel, setEnvDel] = useState(true);
  const [envRows, setEnvRows] = useState([]);

  const envActions = {
    fetch: async () => {
      const envs = await envService.get();
      let id = 0;
      setEnvRows(
        envs.data.map((env) => {
          return { ...env, id: id++ };
        })
      );
    },
    add: async () => {
      const resp = await envService.post({
        name: document.getElementById("env-name").value,
        desc: document.getElementById("env-desc").value,
      });
      if (resp.status == 200) {
        setEnvRows((envRows) => [
          ...envRows,
          { ...resp.data, id: envRows[envRows.length - 1].id + 1 },
        ]);
        envActions.closeAddPrompt();
      }
    },
    delete: async () => {
      const envs = selectedEnvs.map((val) => {
        return { name: envRows[val].name, desc: envRows[val].desc };
      });
      const resp = await envService.delete({ data: envs });
      if (resp.status == 200) {
        envActions.fetch();
        setEnvDel(true);
      }
    },
    select: (newSelection) => {
      if (newSelection.length > 0) setEnvDel(false);
      else setEnvDel(true);
      setSelectedEnvs(newSelection);
    },
    openAddPrompt: () => {
      setOpenEnvAdd(true);
    },
    closeAddPrompt: () => {
      setOpenEnvAdd(false);
    },
  };
  useEffect(() => {
    envService.initialize();
    envActions.fetch();
    onEnvChange(envRows);
  }, [onEnvChange]);
  let actions = (
      <AccordionActions>
        <Button onClick={envActions.openAddPrompt}>Add</Button>
        <Button onClick={envActions.delete} disabled={envDel}>
          Delete
        </Button>
      </AccordionActions>
    ),
    dialogs = (
      <AddEnvDialog
        open={openEnvAdd}
        closeAction={envActions.closeAddPrompt}
        addAction={envActions.add}
      />
    );
  if (!controls) {
    actions = null;
    dialogs = null;
  }
  return (
    <>
      <Accordion>
        <AccordionSummary>Environments</AccordionSummary>
        <AccordionDetails>
          <Box sx={{ height: 400, width: "100%" }}>
            <DataGrid
              rows={envRows}
              columns={envCols}
              initialState={{
                pagination: {
                  paginationModel: { page: 0, pageSize: 10 },
                },
              }}
              pageSizeOptions={[5, 10]}
              checkboxSelection
              onRowSelectionModelChange={envActions.select}
            />
          </Box>
        </AccordionDetails>
        {actions}
      </Accordion>
      {dialogs}
    </>
  );
}
