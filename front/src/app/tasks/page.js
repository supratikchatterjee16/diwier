"use client";
import { Accordion, AccordionDetails, AccordionSummary, Button, Container, Box, AccordionActions } from "@mui/material";
import Toolbar from "../components/Toolbar";
import { DataGrid } from "@mui/x-data-grid";
import { useEffect, useState } from "react";
import axios from "axios";

export default function Tasks() {
    // Initial Data
    const taskColumns = [
        { field: 'name', headerName: 'Task Name', width: 100 },
        { field: 'type', headerName: 'Task Type', width: 200 },
        { field: 'env', headerName: 'Environment', width: 300 },
        { field: 'interval', headerName: 'Interval', width: 200 },
        { field: 'executed', headerName: 'Last Executed', width: 100 },
    ];
    const taskGroupColumns = [
        { field: 'name', headerName: 'Task Name', width: 100 },
        { field: 'env', headerName: 'Environment', width: 300 },
        { field: 'interval', headerName: 'Interval', width: 200 },
        { field: 'executed', headerName: 'Last Executed', width: 100 },
    ];

    // Component logic
    const [taskRows, setTaskRows] = useState([]);
    const fetchTasks = () => {
        axios.get("/api/tasks").then((response) => {
            setTaskRows(response.data);
        }).catch((error) => {
            console.error("Could not fetch tasks.");
        });
    }

    const [tgRows, setTgRows] = useState([]);
    const fetchTaskGroups = () => {
        axios.get("/api/tasks/groups").then((response) => {
            setTgRows(response.data);
        }).catch((error) => {
            console.error("Could not fetch tasks.");
        });
    }

    useEffect(() => {
        if(taskRows.length == 0)
            fetchTasks();
        if(tgRows.length == 0)
            fetchTaskGroups();
    }, []);
    
    // Render
    return (<>
        <Toolbar select="tasks" />
        <Container sx={{ paddingTop: '20pt' }}>
            <Accordion defaultExpanded>
                <AccordionSummary>Tasks</AccordionSummary>
                <AccordionDetails>
                    <Box sx={{ height: 200, width: '100%' }}>
                        <DataGrid
                            rows={taskRows}
                            columns={taskColumns}
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
                    <Button href="/tasks/create">Add New</Button>
                    <Button disabled>Edit</Button>
                    <Button disabled>Delete</Button>
                </AccordionActions>
            </Accordion>

            <Accordion>
                <AccordionSummary>Task Groups</AccordionSummary>
                <AccordionDetails>
                    <Box sx={{ height: 200, width: '100%' }}>
                        <DataGrid
                            rows={tgRows}
                            columns={taskGroupColumns}
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
                    <Button>Add New</Button>
                    <Button disabled>Edit</Button>
                    <Button disabled>Delete</Button>
                </AccordionActions>
            </Accordion>
        </Container>
    </>);
};