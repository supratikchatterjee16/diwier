import { AccountCircle } from '@mui/icons-material';
import { IconButton, Toolbar, Typography } from '@mui/material';
import AppBar from '@mui/material/AppBar';

export default function Header() {
    return (
        <AppBar position="static" color="warning">
            <Toolbar disableGutters>
                <Typography
                    variant="h4" noWrap
                    component="a"
                    href="/"
                    sx={{
                        fontVariant: 'small-caps',
                        letterSpacing: '.2rem',
                        textDecoration: 'none',
                        color: 'white',
                        paddingLeft: '20pt'
                    }}>
                    di-weir
                </Typography>
                <div style={{display: 'flex', flexGrow : 1, flexDirection : 'row-reverse'}}>
                    <IconButton size="xl" aria-label="Sign In">
                        <AccountCircle fontSize='large'/>
                    </IconButton>
                </div>
            </Toolbar>
        </AppBar>
    );
}