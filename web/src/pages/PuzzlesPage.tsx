import React from 'react';
import { Box, Typography, Grid, Card, CardContent, Button, Paper, Chip, Rating } from '@mui/material';
import { styled } from '@mui/material/styles';
import { Chessboard } from 'react-chessboard';

const mockPuzzles = [
  { id: 1, title: 'Mate in 1', difficulty: 'Easy', rating: 4, fen: 'r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3' },
  { id: 2, title: 'Fork the Pieces', difficulty: 'Medium', rating: 5, fen: 'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2' },
  { id: 3, title: 'Endgame Win', difficulty: 'Hard', rating: 3, fen: '8/8/8/4k3/8/4K3/8/8 w - - 0 1' },
  { id: 4, title: 'Skewer Attack', difficulty: 'Medium', rating: 4, fen: 'rnbq1bnr/pp1pkppp/8/2p1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQ - 2 4' },
  { id: 5, title: 'Opening Trap', difficulty: 'Easy', rating: 5, fen: 'r1bqkbnr/pppp1ppp/2n5/4p3/3AP3/5N2/PPP2PPP/RNBQKB1R b KQkq - 0 3' },
  { id: 6, title: 'Defensive Stand', difficulty: 'Hard', rating: 5, fen: 'r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R3K2R w KQ - 2 9' },
];

const difficultyColors: { [key: string]: 'success' | 'warning' | 'error' } = {
  'Easy': 'success',
  'Medium': 'warning',
  'Hard': 'error',
};

const PuzzleCard = styled(Card)(({ theme }) => ({
  transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
  '&:hover': {
    transform: 'scale(1.05)',
    boxShadow: theme.shadows[8],
  },
}));

const PuzzlesPage: React.FC = () => {
  return (
    <Box sx={{ p: 3, backgroundColor: 'white' }}>
      <Typography variant="h4" component="h1" sx={{ mb: 2, fontWeight: 'bold', color: 'primary.dark' }}>
        Puzzle Library
      </Typography>

      {/* Progress Tracker */}
      <Paper elevation={2} sx={{ p: 2, mb: 4, backgroundColor: 'grey.100' }}>
        <Grid container spacing={2} textAlign="center">
          <Grid item xs={12} sm={4}>
            <Typography variant="h6">Puzzles Completed</Typography>
            <Typography variant="h4" color="primary">128</Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6">Success Rate</Typography>
            <Typography variant="h4" color="primary">85%</Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6">Current Streak</Typography>
            <Typography variant="h4" color="primary">12</Typography>
          </Grid>
        </Grid>
      </Paper>

      {/* Puzzle Grid */}
      <Grid container spacing={4}>
        {mockPuzzles.map((puzzle) => (
          <Grid item key={puzzle.id} xs={12} sm={6} md={4}>
            <PuzzleCard>
              <Box sx={{ p: 1, pointerEvents: 'none' }}>
                <Chessboard id={puzzle.id.toString()} position={puzzle.fen} arePiecesDraggable={false} />
              </Box>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                  <Typography variant="h6" component="div">{puzzle.title}</Typography>
                  <Chip label={puzzle.difficulty} color={difficultyColors[puzzle.difficulty]} size="small" />
                </Box>
                <Rating name="read-only" value={puzzle.rating} readOnly />
                <Button variant="contained" fullWidth sx={{ mt: 2, backgroundColor: 'primary.dark' }}>
                  Start Puzzle
                </Button>
              </CardContent>
            </PuzzleCard>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default PuzzlesPage;
