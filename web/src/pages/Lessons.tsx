import React from 'react';
import { Box, Typography, Grid, Card, CardContent, Button, Chip } from '@mui/material';
import SchoolIcon from '@mui/icons-material/School';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';
import PsychologyIcon from '@mui/icons-material/Psychology';

interface Lesson {
  id: number;
  title: string;
  description: string;
  category: 'Openings' | 'Tactics' | 'Endgames' | 'Strategy';
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
}

const lessons: Lesson[] = [
  {
    id: 1,
    title: 'Mastering the Italian Game',
    description: 'Learn the key ideas and variations of one of the most popular openings.',
    category: 'Openings',
    difficulty: 'Beginner',
  },
  {
    id: 2,
    title: 'Essential Tactical Motifs',
    description: 'Recognize common patterns like forks, pins, and skewers to win material.',
    category: 'Tactics',
    difficulty: 'Intermediate',
  },
  {
    id: 3,
    title: 'Rook and Pawn Endgames',
    description: 'Understand the fundamental principles of rook and pawn endings.',
    category: 'Endgames',
    difficulty: 'Advanced',
  },
  {
    id: 4,
    title: 'Positional Understanding',
    description: 'Improve your strategic thinking and learn to create long-term advantages.',
    category: 'Strategy',
    difficulty: 'Intermediate',
  },
];

const getCategoryIcon = (category: string) => {
  switch (category) {
    case 'Openings': return <SchoolIcon />;
    case 'Tactics': return <EmojiEventsIcon />;
    case 'Strategy': return <PsychologyIcon />;
    case 'Endgames': return <SchoolIcon />;
    default: return null;
  }
};

const LessonsPage: React.FC = () => {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={4}>
        {/* Left Column: Title and Description */}
        <Grid item xs={12} md={4}>
          <Box sx={{ p: 2 }}>
            <Typography variant="h3" component="h1" gutterBottom>
              Interactive Lessons
            </Typography>
            <Typography variant="h6" color="text.secondary" paragraph>
              From basic checkmates to advanced positional concepts, our curated lessons are designed to help you master every phase of the game.
            </Typography>
            <Button variant="contained" size="large" sx={{ mt: 2 }}>
              Explore All Lessons
            </Button>
          </Box>
        </Grid>

        {/* Right Column: Lesson Cards */}
        <Grid item xs={12} md={8}>
          <Grid container spacing={3}>
            {lessons.map((lesson) => (
              <Grid item key={lesson.id} xs={12} sm={6}>
                <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', transition: 'transform 0.2s', '&:hover': { transform: 'translateY(-4px)', boxShadow: 6 } }}>
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      {getCategoryIcon(lesson.category)}
                      <Typography variant="subtitle1" color="text.secondary" sx={{ ml: 1 }}>
                        {lesson.category}
                      </Typography>
                    </Box>
                    <Typography variant="h5" component="div" gutterBottom>
                      {lesson.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      {lesson.description}
                    </Typography>
                  </CardContent>
                  <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                     <Chip label={lesson.difficulty} size="small" />
                     <Button size="small" variant="outlined">Start Lesson</Button>
                  </Box>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
};

export default LessonsPage;
