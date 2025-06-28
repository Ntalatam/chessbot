import { createTheme } from '@mui/material/styles';

// Augment the palette to include custom color properties
declare module '@mui/material/styles' {
  interface Palette {
    cream: Palette['primary'];
    tan: Palette['primary'];
  }
  interface PaletteOptions {
    cream?: PaletteOptions['primary'];
    tan?: PaletteOptions['primary'];
  }
}

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#22C55E', // Chess Coach Green
    },
    secondary: {
      main: '#D2B68A', // Tan/Gold
    },
    cream: {
      main: '#EEE5D9',
    },
    tan: {
      main: '#D2B68A',
    },
    background: {
      default: '#0D2A4C', // Darkest Blue
      paper: '#222D52',   // Navy for Cards/Bubbles
    },
    text: {
      primary: '#EEE5D9', // Cream
      secondary: '#D2B68A', // Tan/Gold
    },
    error: {
      main: '#f44336',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", sans-serif',
    h1: { fontSize: '2.25rem', fontWeight: 700 },
    h2: { fontSize: '2rem', fontWeight: 700 },
    h3: { fontSize: '1.875rem', fontWeight: 600 },
    h4: { fontSize: '1.75rem', fontWeight: 600 },
    h6: { fontSize: '1.25rem', fontWeight: 600 },
    body1: { fontSize: '1.125rem', lineHeight: 1.6 },
    body2: { fontSize: '1rem', lineHeight: 1.6 },
    button: {
      textTransform: 'none',
      fontWeight: 'bold',
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '8px',
          boxShadow: 'none',
          transition: 'background-color 0.3s ease, transform 0.2s ease',
          '&:hover': {
            transform: 'scale(1.03)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: '16px',
          boxShadow: 'none',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          backgroundColor: '#222D52',
        },
      },
    },
  },
});

export default theme;
