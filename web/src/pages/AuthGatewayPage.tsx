import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button, Typography, Grid, Paper, SvgIcon } from '@mui/material';


const ChessLogo = () => (
  <Box
    component="img"
    sx={{
      height: 120,
      width: 120,
    }}
    alt="Chess Coach logo"
    src="/assets/logo-icon.png"
  />
);

export default function AuthGatewayPage() {
  const navigate = useNavigate();

  return (
    <Grid container component="main" sx={{ height: '100vh', backgroundColor: 'black' }}>
      <Grid item xs={12} sm={6} md={7} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <ChessLogo />
      </Grid>
      <Grid item xs={12} sm={6} md={5} component={Paper} elevation={6} square sx={{ backgroundColor: 'black', display: 'flex', flexDirection: 'column', justifyContent: 'center', p: 4 }}>
        <Box>
          <Typography component="h1" variant="h2" sx={{ color: 'white', fontWeight: 'bold', mb: 2 }}>
            Happening now
          </Typography>
          <Typography component="h2" variant="h4" sx={{ color: 'white', fontWeight: 'bold', mb: 4 }}>
            Join today.
          </Typography>

          <Button fullWidth variant="contained" sx={{ mb: 1, backgroundColor: 'white', color: 'black', '&:hover': { backgroundColor: '#e0e0e0' } }} disabled>
            Sign up with Google
          </Button>
          <Button fullWidth variant="contained" sx={{ mb: 2, backgroundColor: 'white', color: 'black', '&:hover': { backgroundColor: '#e0e0e0' } }} disabled>
            Sign up with Apple
          </Button>

          <Typography align="center" sx={{ color: 'white', my: 1 }}>or</Typography>

          <Button fullWidth variant="contained" sx={{ mb: 2, backgroundColor: '#1d9bf0', '&:hover': { backgroundColor: '#1a8cd8' } }} onClick={() => navigate('/register')}>
            Create account
          </Button>

          <Typography variant="body2" sx={{ color: 'grey.500', mb: 4 }}>
            By signing up, you agree to the Terms of Service and Privacy Policy, including Cookie Use.
          </Typography>

          <Typography variant="h6" sx={{ color: 'white', fontWeight: 'bold', mb: 2 }}>
            Already have an account?
          </Typography>
          <Button fullWidth variant="outlined" sx={{ color: '#1d9bf0', borderColor: '#536471' }} onClick={() => navigate('/login')}>
            Sign in
          </Button>
        </Box>
      </Grid>
    </Grid>
  );
}
