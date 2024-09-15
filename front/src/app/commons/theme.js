'use client';
import { createTheme } from '@mui/material/styles';
// Note : Due to static build, dynamic selection of themes is a bit trickier than normal.
// Primary effect is that when the page pre-renders, the theme values are all null
// resulting hooks not being available. Workaround for this is yet to be established.
// One way is to convert the handling mechanism to Raw JS, sidestepping MUI's themeing mechanism completely.
// But this will result in having to rewire a lot of things.
// Another is to use CSS for the auxillary theme, and inject a class name at component mount, forcing selection of theme over default colours provided.

// Light theme
export const lightTheme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#ff4081',
    },
    background: {
      default: '#f4f6f8',
    },
  },
  typography: {
    h1: {
      fontSize: '2.5rem',
      fontWeight: 'bold',
    },
    body1: {
      fontSize: '1rem',
    },
  },
});

// Dark theme
export const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#bb86fc',
    },
    secondary: {
      main: '#03dac5',
    },
    background: {
      default: '#121212',
      paper: '#1d1d1d',
    },
    text: {
      primary: '#ffffff',
    },
  },
  typography: {
    h1: {
      fontSize: '2.5rem',
      fontWeight: 'bold',
    },
    body1: {
      fontSize: '1rem',
    },
  },
});
