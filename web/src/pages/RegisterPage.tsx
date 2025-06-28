import React, { useState } from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { authApi } from '../services/authApi';
import {
  Button,
  TextField,
  Container,
  Typography,
  Box,
  Alert,
  CircularProgress,
  Link,
  Grid
} from '@mui/material';

export default function RegisterPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError('');
    setLoading(true);
    try {
      await authApi.register({ username, email, password });
      navigate('/login');
    } catch (err) {
      setError('Failed to register. The email or username may already be taken.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container component="main" maxWidth="xs" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh', backgroundColor: 'black' }}>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          p: 4,
          borderRadius: 2,
          backgroundColor: 'black',
          border: '1px solid #2f3336',
          width: '100%',
        }}
      >
        <Typography component="h1" variant="h5" sx={{ color: 'white', mb: 3, fontWeight: 'bold' }}>
          Create your account
        </Typography>
        {error && <Alert severity="error" sx={{ mb: 2, width: '100%' }}>{error}</Alert>}
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ width: '100%' }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            autoComplete="username"
            autoFocus
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            InputLabelProps={{ sx: { color: 'grey.500' } }}
            sx={{ input: { color: 'white' }, '& .MuiOutlinedInput-root': { '& fieldset': { borderColor: 'grey.700' }, '&:hover fieldset': { borderColor: 'white' } } }}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label="Email Address"
            name="email"
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            InputLabelProps={{ sx: { color: 'grey.500' } }}
            sx={{ input: { color: 'white' }, '& .MuiOutlinedInput-root': { '& fieldset': { borderColor: 'grey.700' }, '&:hover fieldset': { borderColor: 'white' } } }}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="new-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            InputLabelProps={{ sx: { color: 'grey.500' } }}
            sx={{ input: { color: 'white' }, '& .MuiOutlinedInput-root': { '& fieldset': { borderColor: 'grey.700' }, '&:hover fieldset': { borderColor: 'white' } } }}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            disabled={loading}
            sx={{ mt: 3, mb: 2, backgroundColor: '#1d9bf0', '&:hover': { backgroundColor: '#1a8cd8' } }}
          >
            {loading ? <CircularProgress size={24} /> : 'Create account'}
          </Button>
          <Grid container justifyContent="flex-end">
            <Grid item>
              <Link component={RouterLink} to="/login" variant="body2" sx={{ color: '#1d9bf0' }}>
                Already have an account? Sign in
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
}
