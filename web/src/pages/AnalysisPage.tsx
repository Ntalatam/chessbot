import React, { useState, useCallback, useMemo } from 'react';
import { Box, Typography, Grid, Card, CardContent, Button, Paper, CircularProgress, IconButton, SvgIcon, Alert } from '@mui/material';
import { styled, useTheme } from '@mui/material/styles';
import { useDropzone } from 'react-dropzone';
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import { analysisAPI } from '../services/api';

const DropzonePaper = styled(Paper)(({ theme }) => ({
  border: `2px dashed ${theme.palette.text.secondary}`,
  padding: theme.spacing(4),
  textAlign: 'center',
  cursor: 'pointer',
  backgroundColor: 'transparent',
  color: theme.palette.text.secondary,
  transition: 'border-color 0.3s ease',
  '&:hover': {
    borderColor: theme.palette.secondary.main,
    color: theme.palette.secondary.main,
  },
}));

const KnightIconFixed = styled(SvgIcon)(({ theme }) => ({
  position: 'fixed',
  bottom: theme.spacing(4),
  right: theme.spacing(4),
  fontSize: '90px',
  color: theme.palette.secondary.main,
  opacity: 0.25,
  pointerEvents: 'none',
  transform: 'rotate(-15deg)',
}));

const AnalysisPage: React.FC = () => {
  const [pgn, setPgn] = useState<string>('');
  const [game, setGame] = useState<Chess | null>(null);
  const [fen, setFen] = useState<string>('start');
  const [history, setHistory] = useState<any[]>([]);
  const [currentMove, setCurrentMove] = useState<number>(-1);

  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [analysis, setAnalysis] = useState<any>(null);
  const [error, setError] = useState<string>('');
  const theme = useTheme();

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const pgnString = reader.result as string;
        const newGame = new Chess();
        newGame.loadPgn(pgnString);
        setPgn(pgnString);
        setGame(newGame);
        setHistory(newGame.history({ verbose: true }));
        setFen(newGame.fen());
        setAnalysis(null);
        setError('');
        setCurrentMove(newGame.history().length - 1);
      } catch (e) {
        setError('Invalid PGN file. Please upload a valid game.');
        setGame(null);
      }
    };
    reader.readAsText(file);
  }, []);

  const { getRootProps, getInputProps } = useDropzone({ onDrop, accept: { 'application/x-chess-pgn': ['.pgn'] } });

  const handleAnalyze = async () => {
    if (!pgn) {
      setError('Please import a PGN file first.');
      return;
    }
    setIsAnalyzing(true);
    setError('');
    try {
      const response = await analysisAPI.analyzeGame(pgn);
      setAnalysis(response.data);
    } catch (err) {
      setError('Failed to analyze the game. The server might be busy.');
      console.error(err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const navigateToMove = (moveIndex: number) => {
    if (!game || moveIndex < -1 || moveIndex >= history.length) return;

    const tempGame = new Chess();
    if (moveIndex === -1) {
      // Initial position
    } else {
      const moves = game.history().slice(0, moveIndex + 1);
      moves.forEach(move => tempGame.move(move));
    }
    setFen(tempGame.fen());
    setCurrentMove(moveIndex);
  };

  const handlePrevMove = () => navigateToMove(currentMove - 1);
  const handleNextMove = () => navigateToMove(currentMove + 1);

  return (
    <Box sx={{ p: 4, minHeight: 'calc(100vh - 64px)' }}>
      <Typography variant="h4" component="h1" sx={{ mb: 4, fontWeight: 'bold' }}>
        Game Analysis
      </Typography>
      <Grid container spacing={4}>
        <Grid item xs={12} md={5}>
          <Card sx={{ p: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>Import Your Game</Typography>
              <DropzonePaper {...getRootProps()} sx={{ mt: 3, mb: 3 }}>
                <input {...getInputProps()} />
                <UploadFileIcon sx={{ fontSize: 48, mb: 2 }} />
                <Typography variant="body1">Drag & drop a PGN file here, or click</Typography>
              </DropzonePaper>
              {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
              <Button variant="contained" color="secondary" fullWidth sx={{ py: 1.5 }} onClick={handleAnalyze} disabled={isAnalyzing || !game}>
                {isAnalyzing ? <CircularProgress size={24} color="inherit" /> : 'Analyze Game'}
              </Button>
            </CardContent>
          </Card>
          {analysis && (
            <Card sx={{ p: 2, mt: 4 }}>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2 }}>Move Evaluations</Typography>
                <Box sx={{ height: 200, mb: 3 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={analysis.evaluations} margin={{ top: 5, right: 20, left: -20, bottom: 5 }}>
                      <defs>
                        <linearGradient id="colorEval" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor={theme.palette.secondary.main} stopOpacity={0.8}/>
                          <stop offset="95%" stopColor={theme.palette.secondary.main} stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.2)" />
                      <XAxis dataKey="move" stroke={theme.palette.text.secondary} />
                      <YAxis stroke={theme.palette.text.secondary} />
                      <Tooltip contentStyle={{ backgroundColor: theme.palette.background.paper, border: `1px solid ${theme.palette.text.secondary}` }} />
                      <Area type="monotone" dataKey="eval" stroke={theme.palette.secondary.main} fillOpacity={1} fill="url(#colorEval)" />
                    </AreaChart>
                  </ResponsiveContainer>
                </Box>
              </CardContent>
            </Card>
          )}
        </Grid>

        <Grid item xs={12} md={7}>
          <Card sx={{ p: 2, minHeight: '100%' }}>
            <CardContent>
              <Box sx={{ mb: 2 }}>
                <Chessboard
                  position={fen}
                  boardWidth={500}
                  customDarkSquareStyle={{ backgroundColor: '#58ACFA' }}
                  customLightSquareStyle={{ backgroundColor: '#FFFFFF' }}
                />
              </Box>
              {isAnalyzing && (
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                  <CircularProgress color="secondary" />
                  <Typography sx={{ ml: 2 }}>AI is analyzing your game...</Typography>
                </Box>
              )}
              {analysis && (
                <Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="h6">Annotated Moves</Typography>
                    <Box>
                      <IconButton color="secondary" onClick={handlePrevMove} disabled={currentMove < 0}><ArrowBackIcon /></IconButton>
                      <IconButton color="secondary" onClick={handleNextMove} disabled={currentMove >= history.length - 1}><ArrowForwardIcon /></IconButton>
                    </Box>
                  </Box>
                  <Paper variant="outlined" sx={{ p: 2, mt: 1, maxHeight: 250, overflowY: 'auto', backgroundColor: 'transparent', borderColor: 'rgba(255, 255, 255, 0.2)' }}>
                    {analysis.moves.map((m: any, i: number) => (
                      <Typography key={i} onClick={() => navigateToMove(i)} sx={{
                        fontFamily: 'monospace', fontSize: '1.1rem', p: 0.5, borderRadius: 1, cursor: 'pointer',
                        backgroundColor: i === currentMove ? theme.palette.action.hover : 'transparent',
                        '&:hover': { backgroundColor: theme.palette.action.hover }
                      }}>
                        {`${Math.floor(i / 2) + 1}. ${i % 2 === 0 ? '' : '...'}${m.move} - ${m.annotation}`}
                      </Typography>
                    ))}
                  </Paper>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      <KnightIconFixed viewBox="0 0 24 24">
        <path d="M22,8C22,6.67,21.04,5.5,19.75,5.5C19.5,5.5,19.25,5.55,19,5.6L17.88,2.55C17.63,1.95,17.06,1.5,16.4,1.5C15.55,1.5,14.83,2.22,14.83,3.08C14.83,3.34,14.9,3.59,15.03,3.81L13.2,10.26C11.93,10.03,10.59,9.95,9.2,10.03C6.3,10.25,4,12.5,4,15.5C4,18.53,6.47,21,9.5,21C12.53,21,15,18.53,15,15.5C15,14.5,14.75,13.5,14.25,12.75C15.31,12.5,16.25,12,17,11.25L18.5,18.5L20.5,18.5C21.33,18.5,22,17.83,22,17V8Z" />
      </KnightIconFixed>
    </Box>
  );
};

export default AnalysisPage;
