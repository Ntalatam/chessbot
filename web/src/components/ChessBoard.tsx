import React, { useState, useEffect, useCallback } from 'react';
import { Chess } from 'chess.js';
import { Chessboard } from 'react-chessboard';

interface ChessBoardProps {
  position?: string;
  onMove?: (move: any) => void;
  interactive?: boolean;
  width?: number | string;
  orientation?: 'white' | 'black';
  showCoordinates?: boolean;
  customBoardStyle?: React.CSSProperties;
}

const ChessBoard: React.FC<ChessBoardProps> = ({
  position = 'start',
  onMove,
  interactive = true,
  width = 600,
  orientation = 'white',
  showCoordinates = true,
  customBoardStyle = {},
}) => {
  const [game, setGame] = useState<Chess>();
  const [moveHistory, setMoveHistory] = useState<string[]>([]);
  const [fen, setFen] = useState<string>('');

  // Initialize the game
  useEffect(() => {
    const chess = new Chess();
    if (position !== 'start') {
      try {
        chess.load(position);
      } catch (e) {
        console.error('Invalid FEN or PGN:', e);
      }
    }
    setGame(chess);
    setFen(chess.fen());
  }, [position]);

  // Make a move
  const makeMove = useCallback(
    (move: any) => {
      if (!game || !interactive) return false;

      try {
        const result = game.move(move);
        if (result) {
          setFen(game.fen());
          setMoveHistory((prev) => [...prev, result.san]);
          if (onMove) {
            onMove({
              from: result.from,
              to: result.to,
              promotion: result.promotion,
              san: result.san,
              fen: game.fen(),
              pgn: game.pgn(),
            });
          }
          return true;
        }
      } catch (e) {
        console.error('Invalid move:', e);
      }
      return false;
    },
    [game, interactive, onMove]
  );

  // Handle piece movement
  const onDrop = (sourceSquare: string, targetSquare: string, piece: string) => {
    if (!interactive) return false;

    try {
      const move = {
        from: sourceSquare,
        to: targetSquare,
        promotion: piece[1].toLowerCase() ?? 'q', // Always promote to queen for simplicity
      };

      return makeMove(move);
    } catch (e) {
      console.error('Error making move:', e);
      return false;
    }
  };

  // Reset the board to the initial position
  const resetBoard = () => {
    if (!game) return;
    game.reset();
    setFen(game.fen());
    setMoveHistory([]);
  };

  // Go back one move
  const undoMove = () => {
    if (!game || moveHistory.length === 0) return;

    game.undo();
    setFen(game.fen());
    setMoveHistory((prev) => prev.slice(0, -1));
  };

  if (!game) {
    return <div>Loading chess board...</div>;
  }

  return (
    <div style={{ width: typeof width === 'string' ? width : `${width}px`, maxWidth: typeof width === 'string' ? '100%' : `${width}px` }}>
      <Chessboard
        position={fen}
        onPieceDrop={onDrop}
        boardOrientation={orientation}
        areArrowsAllowed={true}
        customBoardStyle={{
          borderRadius: '4px',
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
          ...customBoardStyle,
        }}
        customDarkSquareStyle={{ backgroundColor: '#779556' }}
        customLightSquareStyle={{ backgroundColor: '#ebecd0' }}
        boardWidth={typeof width === 'number' ? width : undefined}
      />
      
      {interactive && (
        <div style={{ marginTop: '16px', display: 'flex', gap: '8px' }}>
          <button 
            onClick={resetBoard}
            style={{
              padding: '8px 16px',
              backgroundColor: '#f0f0f0',
              border: '1px solid #ddd',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            Reset Board
          </button>
          <button 
            onClick={undoMove}
            disabled={moveHistory.length === 0}
            style={{
              padding: '8px 16px',
              backgroundColor: '#f0f0f0',
              border: '1px solid #ddd',
              borderRadius: '4px',
              cursor: moveHistory.length === 0 ? 'not-allowed' : 'pointer',
              opacity: moveHistory.length === 0 ? 0.5 : 1,
            }}
          >
            Undo Move
          </button>
        </div>
      )}
      
      {showCoordinates && moveHistory.length > 0 && (
        <div style={{ marginTop: '16px' }}>
          <h4>Move History:</h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
            {moveHistory.map((move, index) => (
              <span key={index} style={{ marginRight: '8px' }}>
                {index % 2 === 0 ? `${Math.floor(index / 2) + 1}.` : ''} {move}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ChessBoard;
