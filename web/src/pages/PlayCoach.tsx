import React, { useState, useMemo, useEffect } from 'react';
import { Box, Typography, Button, Paper, Grid, Slider, Switch, FormControlLabel, CircularProgress, Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions } from '@mui/material';
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js';
import ReplayIcon from '@mui/icons-material/Replay';
import FlagIcon from '@mui/icons-material/Flag';
import HandshakeIcon from '@mui/icons-material/Handshake';

const PlayCoachPage: React.FC = () => {
  const [game, setGame] = useState(new Chess());
  const [fen, setFen] = useState(game.fen());
  const [isAiThinking, setIsAiThinking] = useState(false);
  const [gameOver, setGameOver] = useState<{ status: string; winner: string } | null>(null);
  const [lastMove, setLastMove] = useState<{ from: string; to: string } | null>(null);

  const moveHistory = useMemo(() => {
    const history = game.history();
    const formattedHistory = [];
    for (let i = 0; i < history.length; i += 2) {
        const moveNumber = Math.floor(i / 2) + 1;
        const whiteMove = history[i];
        const blackMove = history[i + 1] || '';
        formattedHistory.push(`${moveNumber}. ${whiteMove} ${blackMove}`);
    }
    return formattedHistory;
  }, [game]);

  const customSquareStyles = useMemo(() => {
    if (!lastMove) {
      return {};
    }
    return {
      [lastMove.from]: { backgroundColor: 'rgba(255, 255, 0, 0.4)' },
      [lastMove.to]: { backgroundColor: 'rgba(255, 255, 0, 0.4)' },
    };
  }, [lastMove]);

  function makeMove(move: any) {
    const gameCopy = new Chess(game.fen());
    const result = gameCopy.move(move);
    if (result) {
      setGame(gameCopy);
      setFen(gameCopy.fen());
      setLastMove({ from: result.from, to: result.to });
      checkGameOver(gameCopy);
    }
    return result;
  }

  useEffect(() => {
    if (game.turn() === 'b' && !gameOver) { // 'b' is AI's turn
      setIsAiThinking(true);
      setTimeout(() => {
        const possibleMoves = game.moves();
        if (game.isGameOver() || game.isDraw() || possibleMoves.length === 0) {
          setIsAiThinking(false);
          return;
        }
        const randomIndex = Math.floor(Math.random() * possibleMoves.length);
        makeMove(possibleMoves[randomIndex]);
        setIsAiThinking(false);
      }, 1000);
    }
  }, [game, gameOver]);

  function onDrop(sourceSquare: string, targetSquare: string) {
    if (game.turn() !== 'w') return false; // Player is white
    const move = makeMove({ from: sourceSquare, to: targetSquare, promotion: 'q' });
    return move !== null;
  }

  const checkGameOver = (currentGame: Chess) => {
    if (currentGame.isCheckmate()) {
      setGameOver({ status: 'Checkmate', winner: currentGame.turn() === 'w' ? 'Black' : 'White' });
    } else if (currentGame.isDraw()) {
      setGameOver({ status: 'Draw', winner: 'None' });
    }
  };

  const resetGame = () => {
    const newGame = new Chess();
    setGame(newGame);
    setFen(newGame.fen());
    setGameOver(null);
    setLastMove(null);
  };

  return (
    <Box sx={{ p: 3, backgroundColor: 'white' }}>
        <Grid container spacing={2} justifyContent="center">
            <Grid item xs={12} md={8}>
                <Paper elevation={3} sx={{ border: '2px solid', borderColor: 'primary.dark', width: '100%', maxWidth: '700px', margin: 'auto' }}>
                    <Chessboard position={fen} onPieceDrop={onDrop} boardWidth={700} customSquareStyles={customSquareStyles} />
                </Paper>
                <Paper elevation={2} sx={{ p: 2, mt: 2, maxWidth: '700px', margin: 'auto' }}>
                    <Grid container spacing={2} alignItems="center">
                        <Grid item><Button variant="outlined" startIcon={<ReplayIcon />} onClick={resetGame}>New Game</Button></Grid>
                        <Grid item><Button variant="outlined" startIcon={<FlagIcon />}>Resign</Button></Grid>
                        <Grid item><Button variant="outlined" startIcon={<HandshakeIcon />}>Offer Draw</Button></Grid>
                        <Grid item xs><Slider defaultValue={50} aria-label="Difficulty" /></Grid>
                        <Grid item><FormControlLabel control={<Switch />} label="Timer" /></Grid>
                    </Grid>
                </Paper>
            </Grid>
            <Grid item xs={12} md={4}>
                <Paper elevation={3} sx={{ p: 2, height: '748px', overflowY: 'auto', border: '2px solid', borderColor: 'primary.dark' }}>
                    <Typography variant="h6" align="center">Move History</Typography>
                    {isAiThinking && <Box sx={{display: 'flex', justifyContent: 'center', my: 1}}><CircularProgress size={24} /></Box>}
                    <Box>
                        {moveHistory.map((move, index) => (
                            <Typography key={index} sx={{ fontFamily: 'monospace', p: 0.5 }}>{move}</Typography>
                        ))}
                    </Box>
                </Paper>
            </Grid>
        </Grid>

        <Dialog open={!!gameOver}>
            <DialogTitle>{gameOver?.status}</DialogTitle>
            <DialogContent>
                <DialogContentText>{gameOver?.winner !== 'None' ? `${gameOver?.winner} wins!` : 'The game is a draw.'}</DialogContentText>
            </DialogContent>
            <DialogActions>
                <Button onClick={() => alert('Analyze feature coming soon!')}>Analyze Game</Button>
                <Button onClick={resetGame} autoFocus>Play Again</Button>
            </DialogActions>
        </Dialog>
    </Box>
  );
};

export default PlayCoachPage;


