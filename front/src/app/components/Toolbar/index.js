'use client';
import { AppBar, IconButton, Tooltip } from "@mui/material";
import TaskOutlinedIcon from '@mui/icons-material/TaskOutlined';
import DesignServicesOutlinedIcon from '@mui/icons-material/DesignServicesOutlined';
import ScienceOutlinedIcon from '@mui/icons-material/ScienceOutlined';
import HideSourceOutlinedIcon from '@mui/icons-material/HideSourceOutlined';
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import ArchiveOutlinedIcon from '@mui/icons-material/ArchiveOutlined';
import DashboardCustomizeOutlinedIcon from '@mui/icons-material/DashboardCustomizeOutlined';
import { StorageOutlined } from "@mui/icons-material";

export default function Toolbar({ select }) {
    const actions = [
        { action: 'tasks', component: TaskOutlinedIcon },
        { action: 'design', component: DesignServicesOutlinedIcon },
        { action: 'analyze', component: ScienceOutlinedIcon },
        { action: 'anonymize', component: HideSourceOutlinedIcon },
        { action: 'archive', component: ArchiveOutlinedIcon },
        { action: 'purge', component: DeleteOutlinedIcon },
        { action: 'dashboard', component: DashboardCustomizeOutlinedIcon },
        { action: 'databases', component: StorageOutlined },
    ];
    actions.forEach((elem) => {
        if (elem.action === select) {
            elem['select'] = true;
        }
    });

    return (<AppBar position="static" color="transparent">
        <div>
            {
                actions.map(
                    (obj, i) => {
                        return <Tooltip title={obj.action.charAt(0).toUpperCase() + obj.action.slice(1)} key={i + 1}>
                            <IconButton size="large" onClick={() => window.location.replace('/' + obj.action)}>
                                {obj.select ? <obj.component sx={{ color: '#ed6c02' }} /> : <obj.component />}
                            </IconButton>
                        </Tooltip>;
                    }
                )
            }
        </div>
    </AppBar>);
}
