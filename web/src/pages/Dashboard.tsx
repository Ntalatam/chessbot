import React, { useEffect, useState } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Box, Typography, Grid, Card, Paper, List, ListItem, ListItemText, CircularProgress, Alert, Skeleton, CardActionArea, Icon } from '@mui/material';
import { styled } from '@mui/material/styles';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import ExtensionIcon from '@mui/icons-material/Extension';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import SportsEsportsIcon from '@mui/icons-material/SportsEsports';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import VideogameAssetIcon from '@mui/icons-material/VideogameAsset';
import { dashboardAPI } from '../services/api';

// --- Type Definitions ---
interface UserProfile {
  username: string;
  elo: number;
  games_played: number;
  record: { wins: number; losses: number; draws: number };
}

interface ProgressSummary {
  games_played_this_week: number;
  puzzles_solved_this_week: number;
  accuracy_history: { game: number; accuracy: number }[];
}

interface AICoachingTip {
  title: string;
  message: string;
}

interface NewDashboardData {
  user_profile: UserProfile;
  progress_summary: ProgressSummary;
  coaching_feed: AICoachingTip[];
}

// --- Styled Components ---
const QuickAccessCard = styled(Card)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  padding: theme.spacing(3),
  height: '100%',
  textAlign: 'center',
  transition: 'transform 0.2s, box-shadow 0.2s',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: theme.shadows[6],
  },
}));

const StatCard = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  textAlign: 'center',
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
}));

// --- Main Component ---
const Dashboard: React.FC = () => {
  const [data, setData] = useState<NewDashboardData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await dashboardAPI.getNewDashboardData();
        setData(response.data);
      } catch (err) {
        setError('Failed to load dashboard. The server might be busy, or you may need to log in again.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <Box sx={{ p: 3 }}>
        <Skeleton variant="text" width={300} height={60} />
        <Grid container spacing={3} sx={{ mt: 1 }}>
          {[...Array(4)].map((_, i) => (
            <Grid item xs={12} sm={6} md={3} key={i}>
              <Skeleton variant="rounded" height={120} />
            </Grid>
          ))}
          <Grid item xs={12} md={8}>
            <Skeleton variant="rounded" height={200} />
          </Grid>
          <Grid item xs={12} md={4}>
            <Skeleton variant="rounded" height={200} />
          </Grid>
        </Grid>
      </Box>
    );
  }

  if (error || !data) {
    return <Alert severity="error" sx={{ m: 3 }}>{error || 'No data available.'}</Alert>;
  }

  const { user_profile, progress_summary, coaching_feed } = data;

  const quickAccessItems = [
    { title: 'Analyze a Game', icon: <AnalyticsIcon fontSize="large" />, link: '/app/analysis' },
    { title: 'Solve a Puzzle', icon: <ExtensionIcon fontSize="large" />, link: '/app/puzzles' },
    { title: 'Play AI Coach', icon: <SmartToyIcon fontSize="large" />, link: '/app/play' },
    { title: 'Play AI Game', icon: <SportsEsportsIcon fontSize="large" />, link: '/app/play' },
  ];

  return (
    <Box sx={{ p: { xs: 2, sm: 3 } }}>
      {/* Welcome Header */}
      <Typography variant="h4" component="h1" sx={{ mb: 1, fontWeight: 'bold' }}>
        Welcome back, {user_profile.username}!
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" sx={{ mb: 4 }}>
        Ready to improve today?
      </Typography>

      <Grid container spacing={3}>
        {/* Quick Access Tiles */}
        {quickAccessItems.map((item) => (
          <Grid item xs={12} sm={6} md={3} key={item.title}>
            <CardActionArea component={RouterLink} to={item.link} sx={{ borderRadius: 2 }}>
              <QuickAccessCard>
                <Icon color="primary" sx={{ fontSize: '48px !important', mb: 1 }}>{item.icon}</Icon>
                <Typography variant="h6" component="h2">{item.title}</Typography>
              </QuickAccessCard>
            </CardActionArea>
          </Grid>
        ))}

        {/* User Profile Stats */}
        <Grid item xs={12} md={4}>
          <StatCard elevation={2}>
            <EmojiEventsIcon sx={{ fontSize: 40, color: 'primary.main', mx: 'auto' }} />
            <Typography variant="h4" sx={{ fontWeight: 'bold' }}>{user_profile.elo}</Typography>
            <Typography color="text.secondary">Current ELO</Typography>
          </StatCard>
        </Grid>
        <Grid item xs={12} md={4}>
          <StatCard elevation={2}>
            <VideogameAssetIcon sx={{ fontSize: 40, color: 'primary.main', mx: 'auto' }} />
            <Typography variant="h4" sx={{ fontWeight: 'bold' }}>{user_profile.games_played}</Typography>
            <Typography color="text.secondary">Total Games Played</Typography>
          </StatCard>
        </Grid>
        <Grid item xs={12} md={4}>
          <StatCard elevation={2}>
            <CheckCircleOutlineIcon sx={{ fontSize: 40, color: 'primary.main', mx: 'auto' }} />
            <Typography variant="h4" sx={{ fontWeight: 'bold' }}>{`${user_profile.record.wins}W / ${user_profile.record.losses}L / ${user_profile.record.draws}D`}</Typography>
            <Typography color="text.secondary">Win/Loss/Draw Record</Typography>
          </StatCard>
        </Grid>

        {/* Progress Summary */}
        <Grid item xs={12} lg={8}>
          <Card sx={{ p: 2, height: 300 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>Accuracy vs. AI (Last 5 Games)</Typography>
            <ResponsiveContainer width="100%" height="85%">
              <BarChart data={progress_summary.accuracy_history} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="game" />
                <YAxis domain={[0, 100]} />
                <Tooltip cursor={{fill: 'rgba(206, 206, 206, 0.2)'}} />
                <Legend />
                <Bar dataKey="accuracy" fill="#8884d8" name="Move Accuracy (%)" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Grid>
        <Grid item xs={12} lg={4}>
          <Card sx={{ p: 3, height: 300, display: 'flex', flexDirection: 'column', justifyContent: 'space-around' }}>
            <Typography variant="h6">This Week's Progress</Typography>
            <Box>
              <Typography variant="h3" component="p" sx={{ fontWeight: 'bold' }}>{progress_summary.games_played_this_week}</Typography>
              <Typography variant="body1" color="text.secondary">Games Played</Typography>
            </Box>
            <Box>
              <Typography variant="h3" component="p" sx={{ fontWeight: 'bold' }}>{progress_summary.puzzles_solved_this_week}</Typography>
              <Typography variant="body1" color="text.secondary">Puzzles Solved</Typography>
            </Box>
          </Card>
        </Grid>

        {/* Coaching Feed */}
        <Grid item xs={12}>
          <Paper elevation={2} sx={{ p: 3, backgroundColor: 'primary.dark', color: 'white', borderRadius: 2 }}>
            <Typography variant="h5" sx={{ mb: 2, fontWeight: 'bold' }}>AI Coaching Feed</Typography>
            <List>
              {coaching_feed.map((tip, index) => (
                <ListItem key={index} sx={{ py: 1, borderBottom: '1px solid rgba(255, 255, 255, 0.1)' }}>
                  <ListItemText 
                    primary={tip.title}
                    secondary={tip.message}
                    primaryTypographyProps={{ fontWeight: 'bold', color: 'secondary.light' }}
                    secondaryTypographyProps={{ sx: { color: 'white', opacity: 0.9 } }}
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
