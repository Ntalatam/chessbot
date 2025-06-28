import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button, Container, Grid, Typography, Paper, Avatar } from '@mui/material';
import { styled, useTheme } from '@mui/material/styles';
import { Chessboard } from 'react-chessboard';

// Icons
import PsychologyIcon from '@mui/icons-material/Psychology';
import TrackChangesIcon from '@mui/icons-material/TrackChanges';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import BoltIcon from '@mui/icons-material/Bolt';
import GroupsIcon from '@mui/icons-material/Groups';
import StarIcon from '@mui/icons-material/Star';
import TwitterIcon from '@mui/icons-material/Twitter';
import YouTubeIcon from '@mui/icons-material/YouTube';
import EmailIcon from '@mui/icons-material/Email';

const LandingPageContainer = styled(Box)({ 
  backgroundColor: '#FFFFFF',
  color: '#10182B',
});

const HeroSection = styled(Container)(({ theme }) => ({
  padding: theme.spacing(10, 2),
  textAlign: 'left',
}));

const FeatureSection = styled(Box)(({ theme }) => ({
  padding: theme.spacing(12, 2),
  backgroundColor: '#F9FAFB',
  textAlign: 'center',
}));

const TestimonialSection = styled(Box)(({ theme }) => ({
  padding: theme.spacing(12, 2),
  textAlign: 'center',
}));

const CtaSection = styled(Box)(({ theme }) => ({
  padding: theme.spacing(10, 2),
  backgroundColor: '#22C55E',
  color: '#FFFFFF',
  textAlign: 'center',
}));

const Footer = styled(Box)(({ theme }) => ({
  padding: theme.spacing(6, 2),
  backgroundColor: '#10182B',
  color: '#E0E0E0',
}));

const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const theme = useTheme();

  const handleNavigate = (path: string) => {
    navigate(path);
  };

  const handleScrollTo = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <LandingPageContainer>
      {/* Hero Section */}
      <HeroSection maxWidth="lg">
        <Grid container spacing={8} alignItems="center">
          <Grid item xs={12} md={6}>
            <Box sx={{ mb: 4 }}>
              <img src="/assets/logo-banner.png" alt="Chess Coach Logo" style={{ height: '50px' }} />
            </Box>
            <Typography variant="h2" component="h1" sx={{ fontWeight: 'bold', mb: 2 }}>
              Master Chess with Your Personal <span style={{ color: '#22C55E' }}>AI Grandmaster</span>
            </Typography>
            <Typography variant="h6" color="text.secondary" sx={{ mb: 4 }}>
              Play against an intelligent AI coach that adapts to your skill level and provides real-time feedback to accelerate your chess improvement.
            </Typography>
            <Box>
              <Button variant="contained" size="large" sx={{ mr: 2, backgroundColor: '#22C55E', '&:hover': { backgroundColor: '#16A34A' } }} onClick={() => navigate('/auth')}>
                Start Playing Now
              </Button>
              <Button variant="outlined" size="large" onClick={() => handleScrollTo('why-choose-chess-coach')}>
                See How It Works
              </Button>
            </Box>
            <Grid container spacing={4} sx={{ mt: 4 }}>
              {[{label: 'Active Players', value: '50K+'}, {label: 'Games Played', value: '1M+'}, {label: 'User Rating', value: '4.9★'}].map(stat => (
                <Grid item key={stat.label}>
                  <Typography variant="h5" sx={{ fontWeight: 'bold' }}>{stat.value}</Typography>
                  <Typography variant="body1" color="text.secondary">{stat.label}</Typography>
                </Grid>
              ))}
            </Grid>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper elevation={4} sx={{ p: 2, borderRadius: '12px', backgroundColor: '#F9FAFB' }}>
              <Chessboard boardWidth={400} position="r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3" />
              <Box sx={{ mt: 2, p: 2, backgroundColor: 'white', borderRadius: '8px', display: 'flex', alignItems: 'center' }}>
                <Avatar sx={{ bgcolor: '#22C55E', mr: 2 }}>AI</Avatar>
                <Typography variant="body1">"Great opening move! You're controlling the center. Consider developing your knights next."</Typography>
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </HeroSection>

      {/* Features Section */}
      <FeatureSection id="why-choose-chess-coach">
        <Container maxWidth="md">
          <Box sx={{ flexGrow: 1 }}>
            <img src="/assets/logo-banner.png" alt="Chess Coach Logo" style={{ height: '40px' }} />
          </Box>
          <Typography variant="h6" color="text.secondary" sx={{ mb: 8 }}>
            Experience the future of chess learning with our AI-powered platform designed for players of all levels.
          </Typography>
        </Container>
        <Container maxWidth="lg">
          <Grid container spacing={4}>
            {[
              { icon: <PsychologyIcon fontSize="large" sx={{ color: '#22C55E' }} />, title: 'AI-Powered Analysis', description: 'Get instant feedback on every move with explanations from our advanced AI coach.' },
              { icon: <TrackChangesIcon fontSize="large" sx={{ color: '#22C55E' }} />, title: 'Personalized Training', description: 'Adaptive difficulty that matches your skill level and helps you improve consistently.' },
              { icon: <TrendingUpIcon fontSize="large" sx={{ color: '#22C55E' }} />, title: 'Track Your Progress', description: 'Detailed analytics and progress tracking to see your improvement over time.' },
              { icon: <MenuBookIcon fontSize="large" sx={{ color: '#22C55E' }} />, title: 'Learn Openings', description: 'Master chess openings with guided practice and expert explanations.' },
              { icon: <BoltIcon fontSize="large" sx={{ color: '#22C55E' }} />, title: 'Instant Feedback', description: 'Real-time commentary during your games to help you make better decisions.' },
              { icon: <GroupsIcon fontSize="large" sx={{ color: '#22C55E' }} />, title: 'Community Driven', description: 'Join thousands of players all improving their chess skills together.' },
            ].map(feature => (
              <Grid item xs={12} md={4} key={feature.title}>
                <Paper elevation={0} sx={{ p: 3, textAlign: 'left', backgroundColor: 'white', borderRadius: '12px' }}>
                  {feature.icon}
                  <Typography variant="h6" sx={{ fontWeight: 'bold', my: 1 }}>{feature.title}</Typography>
                  <Typography variant="body1" color="text.secondary">{feature.description}</Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Container>
      </FeatureSection>

      {/* Testimonials Section */}
      <TestimonialSection>
        <Container maxWidth="md">
          <Typography variant="h3" component="h2" sx={{ fontWeight: 'bold', mb: 2 }}>Success Stories</Typography>
          <Typography variant="h6" color="text.secondary" sx={{ mb: 8 }}>
            Join thousands of players who have dramatically improved their chess with our AI coaching.
          </Typography>
        </Container>
        <Container maxWidth="lg">
          <Grid container spacing={4}>
            {[
              { name: 'Jessica P.', role: 'Expert Player', rating: '2150 → 2380', quote: 'The AI coaching is incredible. It identified patterns in my play that I never noticed and helped me break through to expert level in just 6 months.', avatar: '/static/images/avatar/1.jpg' },
              { name: 'Michael B.', role: 'Intermediate Player', rating: '1200 → 1650', quote: 'As a beginner, I was overwhelmed by chess theory. The personalized lessons made everything click. My rating jumped 450 points!', avatar: '/static/images/avatar/2.jpg' },
              { name: 'Sarah L.', role: 'Advanced Player', rating: '1800 → 2100', quote: 'The real-time analysis during games is a game-changer. It’s like having a grandmaster whispering perfect moves in your ear.', avatar: '/static/images/avatar/3.jpg' },
            ].map(t => (
              <Grid item xs={12} md={4} key={t.name}>
                <Paper elevation={0} sx={{ p: 3, border: '1px solid #E0E0E0', borderRadius: '12px', height: '100%' }}>
                  <Box sx={{ display: 'flex', color: '#FBBF24' }}>
                    {[...Array(5)].map((_, i) => <StarIcon key={i} />)}
                  </Box>
                  <Typography variant="body1" sx={{ my: 2, fontStyle: 'italic' }}>"{t.quote}"</Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Avatar src={t.avatar} alt={t.name} sx={{ mr: 2 }} />
                    <Box>
                      <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>{t.name}</Typography>
                      <Typography variant="body2" color="text.secondary">{t.role} <span style={{ color: '#22C55E' }}>{t.rating}</span></Typography>
                    </Box>
                  </Box>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Container>
      </TestimonialSection>

      {/* CTA Section */}
      <CtaSection>
        <Container maxWidth="md">
          <Typography variant="h2" component="h2" sx={{ fontWeight: 'bold', mb: 2 }}>Ready to Master Chess?</Typography>
          <Typography variant="h6" sx={{ mb: 4, opacity: 0.9 }}>
            Join thousands of players who are improving their chess skills with our AI-powered coaching platform.
          </Typography>
                    <Button variant="contained" size="large" sx={{ backgroundColor: 'white', color: '#16A34A', '&:hover': { backgroundColor: '#F0F0F0' } }} onClick={() => handleNavigate('/app')}>
            Start Playing Free
          </Button>
          <Typography variant="body2" sx={{ mt: 2, opacity: 0.8 }}>
            ✓ Free to start ✓ No credit card required ✓ Instant access
          </Typography>
        </Container>
      </CtaSection>

      {/* Footer */}
      <Footer>
        <Container maxWidth="lg">
          <Grid container spacing={4} justifyContent="space-between">
            <Grid item xs={12} md={4}>
              
              <Typography variant="body2" sx={{ mb: 2, maxWidth: '300px' }}>
                Master chess with AI-powered coaching that adapts to your skill level and accelerates your improvement.
              </Typography>
              <Box>
                <TwitterIcon sx={{ mr: 1 }} />
                <YouTubeIcon sx={{ mr: 1 }} />
                <EmailIcon />
              </Box>
            </Grid>
            <Grid item xs={6} md={2}>
              <Typography variant="overline">Product</Typography>
              <Box component="ul" sx={{ p: 0, m: 0, listStyle: 'none' }}>
                <li><Button sx={{ p: 0, color: '#E0E0E0', textTransform: 'none' }} onClick={() => handleNavigate('/app/play-ai')}>Play AI</Button></li>
                <li><Button sx={{ p: 0, color: '#E0E0E0', textTransform: 'none' }} onClick={() => handleNavigate('/app/puzzles')}>Puzzles</Button></li>
                <li><Button sx={{ p: 0, color: '#E0E0E0', textTransform: 'none' }} onClick={() => handleNavigate('/app/analysis')}>Analysis</Button></li>
              </Box>
            </Grid>
            <Grid item xs={6} md={2}>
              <Typography variant="overline">Support</Typography>
              <Box component="ul" sx={{ p: 0, m: 0, listStyle: 'none' }}>
                <li><Button sx={{ p: 0, color: '#E0E0E0', textTransform: 'none' }}>Help Center</Button></li>
                <li><Button sx={{ p: 0, color: '#E0E0E0', textTransform: 'none' }}>Contact</Button></li>
                <li><Button sx={{ p: 0, color: '#E0E0E0', textTransform: 'none' }}>Privacy</Button></li>
                <li><Button sx={{ p: 0, color: '#E0E0E0', textTransform: 'none' }}>Terms</Button></li>
              </Box>
            </Grid>
          </Grid>
          <Typography variant="body2" sx={{ mt: 6, textAlign: 'center', borderTop: '1px solid #333', pt: 4 }}>
            © {new Date().getFullYear()} Chess Coach AI. All Rights Reserved.
          </Typography>
        </Container>
      </Footer>
    </LandingPageContainer>
  );
};

export default LandingPage;
