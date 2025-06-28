import React, { useState, useMemo, useCallback } from 'react';
import { Box, Typography, Grid, Paper, Button, TextField, CircularProgress, Card, CardContent, List, ListItem, ListItemText, Divider } from '@mui/material';
import { analysisAPI } from '../services/api';
import ChessBoard from '../components/ChessBoard';
import { Chess, Move } from 'chess.js';

// Type definitions for analysis data
interface EvaluationScore {
  unit: 'cp' | 'mate';
  value: number;
}

interface TopMove {
  move: string;
  score: EvaluationScore;
}

interface PositionAnalysis {
  evaluation: EvaluationScore;
  top_moves: TopMove[];
}

const pgnPlaceholder = `[Event "Your Game"]
[Site "Your Computer"]
[Date "2023.10.27"]
[Round "1"]
[White "You"]
[Black "Opponent"]
[Result "*"]

1. e4 e5 *`;

const ReviewPage: React.FC = () => {
  const [pgn, setPgn] = useState('');
  const [game, setGame] = useState<Chess | null>(null);
  const [currentMoveIndex, setCurrentMoveIndex] = useState(-1);
  const [analysis, setAnalysis] = useState<PositionAnalysis | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const history: Move[] = useMemo(() => game?.history({ verbose: true }) || [], [game]);
  
  const currentFen = useMemo(() => {
    if (!game) return 'start';
    if (currentMoveIndex < 0) return game.fen();
    return history[currentMoveIndex]?.after || game.fen();
  }, [game, history, currentMoveIndex]);

  const handlePgnLoad = useCallback(() => {
    const newGame = new Chess();
    try {
      newGame.load(pgn); // Use .load() for chess.js v1+
      setGame(newGame);
      setCurrentMoveIndex(newGame.history().length - 1);
      setAnalysis(null);
      setError(null);
    } catch (e) {
      setError('Invalid PGN. Please check the format and try again.');
      setGame(null);
    }
  }, [pgn]);

  const handleMoveSelect = (index: number) => {
    setCurrentMoveIndex(index);
    setAnalysis(null); // Clear previous analysis
  };

  const handleAnalysis = async () => {
    if (!currentFen) return;
    setIsAnalyzing(true);
    setAnalysis(null);
    try {
      const response = await analysisAPI.analyzePosition(currentFen);
      setAnalysis(response.data);
    } catch (err) {
      setError('Failed to get analysis from the server.');
    } finally {
      setIsAnalyzing(false);
    }
  };
  
  const getEvalScore = (score: EvaluationScore) => {
    if (score.unit === 'cp') {
      const evalValue = score.value / 100;
      return evalValue > 0 ? `+${evalValue.toFixed(2)}` : evalValue.toFixed(2);
    }
    // Mate in X, e.g., M3 for mate in 3, M-2 for mate in 2 for black
    return `M${score.value}`;
  };

  const evalBarWidth = useMemo(() => {
    if (!analysis) return 50;
    const { unit, value } = analysis.evaluation;
    if (unit === 'mate') {
      return value > 0 ? 100 : 0;
    }
    // Cap centipawn value for visualization, e.g., at +/- 800cp
    const maxCp = 800;
    const cappedValue = Math.max(-maxCp, Math.min(maxCp, value));
    // Scale from 0% to 100%
    return 50 + (cappedValue / (maxCp * 2)) * 100;
  }, [analysis]);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom>Game Analysis</Typography>
      <Grid container spacing={3}>
        {/* Left Column: Board and PGN Input */}
        <Grid item xs={12} md={7}>
          <Card>
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <ChessBoard position={currentFen} interactive={false} width="100%" />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="h6">Move History</Typography>
                  <Paper variant="outlined" sx={{ height: 300, overflowY: 'auto', mt: 1 }}>
                    <List dense>
                      {history.map((move, index) => (
                        <ListItem 
                          button 
                          key={index} 
                          selected={index === currentMoveIndex}
                          onClick={() => handleMoveSelect(index)}
                        >
                          <ListItemText primary={`${Math.floor(index / 2) + 1}${index % 2 === 0 ? '.' : '...'} ${move.san}`} />
                        </ListItem>
                      ))}
                    </List>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>Import PGN</Typography>
              <TextField
                fullWidth
                multiline
                rows={8}
                variant="outlined"
                value={pgn}
                onChange={(e) => setPgn(e.target.value)}
                placeholder={pgnPlaceholder}
              />
              <Button variant="contained" onClick={handlePgnLoad} sx={{ mt: 2 }}>
                Load Game
              </Button>
              {error && <Typography color="error" sx={{ mt: 2 }}>{error}</Typography>}
            </CardContent>
          </Card>
        </Grid>

        {/* Right Column: Analysis Panel */}
        <Grid item xs={12} md={5}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Engine Analysis</Typography>
              <Button 
                variant="contained" 
                onClick={handleAnalysis} 
                disabled={!game || isAnalyzing}
                fullWidth
              >
                {isAnalyzing ? <CircularProgress size={24} /> : 'Analyze Position'}
              </Button>
              
              {analysis && (
                <Box sx={{ mt: 3 }}>
                  <Typography variant="subtitle1">Evaluation: {getEvalScore(analysis.evaluation)}</Typography>
                  <Box sx={{ width: '100%', bgcolor: 'grey.300', borderRadius: 1, overflow: 'hidden', mt: 1 }}>
                     <Box sx={{ 
                         height: 20, 
                         width: `${evalBarWidth}%`, 
                         bgcolor: 'primary.main',
                         transition: 'width 0.3s ease-in-out'
                      }} />
                  </Box>
                  
                  <Typography variant="subtitle1" sx={{ mt: 2 }}>Top Moves:</Typography>
                  <List dense>
                    {analysis.top_moves.map((move: TopMove, index: number) => (
                      <ListItem key={index} divider>
                        <ListItemText primary={move.move} secondary={`Score: ${getEvalScore(move.score)}`} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ReviewPage;
