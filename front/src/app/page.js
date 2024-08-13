import { Box } from "@mui/material";
import Toolbar from "./components/Toolbar";

export default function Home() {
    return (<>
        <Toolbar />
        <Box sx={{
            height: '80vh',
            width: '100%',
            display: 'flex',
            flexDirection: 'row',
            alignItems: 'center',
        }}
        >
            <Box sx={{
                width: '100%',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
            }}
            >
                Nothing to see here. Add a dashboard view.
            </Box>
        </Box>
    </>);
};