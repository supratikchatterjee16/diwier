import { Paper, Typography } from "@mui/material";

export default function Footer(){
    return(
        <Paper>
            <Typography
                variant="subtitle2"
                sx={{
                    textAlign : 'center', 
                    paddingTop : '10pt',
                    color : 'rgba(50, 50, 50, 0.7)'
                }}>
                © 2024 Conceivilize
            </Typography>
            <Typography
                variant="subtitle2"
                sx={{
                    textAlign : 'center', 
                    paddingBottom : '10pt',
                    color : 'rgba(50, 50, 50, 0.7)'
                }}>
                Made using NextJS, MUI, SQLAlchemy
            </Typography>
        </Paper>
    );
}