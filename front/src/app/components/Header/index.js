import { AccountCircle } from '@mui/icons-material';
import { Container, IconButton, Toolbar, Typography } from '@mui/material';
import AppBar from '@mui/material/AppBar';

export default function Header() {
    return (
        <AppBar position="static" color="warning">
            <Container maxWidth="xl">
                <Toolbar disableGutters>
                    <Typography 
                        variant="h6" noWrap 
                        component="a" 
                        href="/"
                        sx={{
                            display : 'flex',
                            fontVariant : 'small-caps',
                            letterSpacing : '.2rem',
                            textDecoration : 'none',
                            color : 'white',
                            flexGrow : 1
                            }}>
                        di-weir
                    </Typography>
                    <div>
                        <IconButton size="large" aria-label="Sign In">
                            <AccountCircle/>
                        </IconButton>
                    </div>
                </Toolbar>
            </Container>
        </AppBar>
    );
}