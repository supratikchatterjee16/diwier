"use client";
import { Accordion, AccordionActions, AccordionDetails, AccordionSummary, Box, Button, Container } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";

import axios from "axios";
import { useEffect, useState } from "react";
import Toolbar from "../components/Toolbar";

export default function DatabasesPage() {
    // Intrinsic Data
    const envCols = [
        { field: 'name', headerName: 'Name', width: 200 },
        { field: 'desc', headerName: 'Description', width: 500 },
    ];
    const conCols = [
        { field: 'name', headerName: 'Name', width: 150 },
        { field: 'env_name', headerName: 'Environment Name', width: 250 },
        { field: 'provider', headerName: 'Provider', width: 150 },
        { field: 'ip', headerName: 'IP', width: 250 },
        { field: 'schema', headerName: 'Schema', width: 100 },
    ];

    // Component logic
    const [envRows, setEnvRows] = useState([]);
    const [conRows, setConRows] = useState([]);
    const fetchEnvs = () => {
        let id = 0;
        axios.get('/api/envs')
        .then((resp) => {
            setEnvRows(resp.data.map((current) => {
                return {...current, id : id++};
            })); 
        })
        .catch((e) => { console.log("Could not fetch environments"); console.error(e);});
    };
    const fetchCons = () => {
        axios.get('/api/conns').then((resp) => { setConRows(resp.data); }).catch(() => { console.log("Could not fetch connections"); });
    };
    useEffect(() => {
        fetchEnvs();
        fetchCons();
    }, []);
    // Rendering
    return (<>
        <Toolbar select="databases" />
        <Container maxWidth="xl" sx={{ paddingTop: '20pt' }}>
            <Accordion>
                <AccordionSummary>Environments</AccordionSummary>
                <AccordionDetails>
                    <Box sx={{ height: 400, width: '100%' }}>
                        <DataGrid
                            rows={envRows}
                            columns={envCols}
                            initialState={{
                                pagination: {
                                    paginationModel: { page: 0, pageSize: 5 },
                                },
                            }}
                            pageSizeOptions={[5, 10]}
                            checkboxSelection
                        ></DataGrid>
                    </Box>
                </AccordionDetails>
                <AccordionActions>
                    <Button>Add</Button>
                    <Button disabled>Delete</Button>
                </AccordionActions>
            </Accordion>
            <Accordion defaultExpanded>
                <AccordionSummary>Connections</AccordionSummary>
                <AccordionDetails>
                    <Box sx={{ height: 500, width: '100%' }}>
                        <DataGrid
                            rows={conRows}
                            columns={conCols}
                            initialState={{
                                pagination: {
                                    paginationModel: { page: 0, pageSize: 50 },
                                },
                            }}
                            pageSizeOptions={[5, 10, 50, 100]}
                            checkboxSelection
                        ></DataGrid>
                    </Box>
                </AccordionDetails>
                <AccordionActions>
                    <Button>Add</Button>
                    <Button disabled>Modify</Button>
                    <Button disabled>Delete</Button>
                </AccordionActions>
            </Accordion>
        </Container>
    </>);
}