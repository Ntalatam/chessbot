import React, { useState, useEffect, useRef } from 'react';
import { Box, Typography, TextField, IconButton, Paper, Avatar, CircularProgress } from '@mui/material';
import { Send as SendIcon, Face as UserIcon, Adb as CoachIcon } from '@mui/icons-material';

interface Message {
  id: string;
  sender: 'user' | 'coach';
  content: string;
  timestamp: string;
}

const initialMessages: Message[] = [
  {
    id: '1',
    sender: 'coach',
    content: 'Hello! I am your AI Chess Coach. Ask me anything about openings, tactics, or strategy.',
    timestamp: new Date().toLocaleTimeString(),
  },
  {
    id: '2',
    sender: 'user',
    content: 'Can you explain the main ideas behind the Sicilian Defense?',
    timestamp: new Date().toLocaleTimeString(),
  },
  {
    id: '3',
    sender: 'coach',
    content: 'Of course! The Sicilian Defense is a dynamic and aggressive response to e4. Black immediately challenges White\'s control of the center and creates an asymmetrical pawn structure, often leading to sharp, tactical battles.',
    timestamp: new Date().toLocaleTimeString(),
  },
];

const CoachChatPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      sender: 'user',
      content: input,
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Simulate API call
    setTimeout(() => {
      const coachResponse: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'coach',
        content: `I'm processing your request about "${input}". This is a simulated response. In a real app, I would provide a detailed explanation. `,
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, coachResponse]);
      setIsLoading(false);
    }, 1500);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 100px)', bgcolor: 'background.default' }}>
      {/* Message Display Area */}
      <Box sx={{ flexGrow: 1, overflowY: 'auto', p: 3 }}>
        {messages.map((msg) => (
          <Box
            key={msg.id}
            sx={{
              display: 'flex',
              justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start',
              mb: 2,
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'flex-start', flexDirection: msg.sender === 'user' ? 'row-reverse' : 'row' }}>
              <Avatar sx={{ bgcolor: msg.sender === 'user' ? 'primary.main' : 'secondary.main', ml: msg.sender === 'user' ? 2 : 0, mr: msg.sender === 'user' ? 0 : 2 }}>
                {msg.sender === 'user' ? <UserIcon /> : <CoachIcon />}
              </Avatar>
              <Paper
                variant="outlined"
                sx={{
                  p: 2,
                  bgcolor: msg.sender === 'user' ? 'primary.light' : 'background.paper',
                  borderRadius: '12px',
                  maxWidth: '70%',
                  border: msg.sender === 'user' ? '1px solid #4caf50' : '1px solid #e0e0e0',
                }}
              >
                <Typography variant="body1">{msg.content}</Typography>
                <Typography variant="caption" color="text.secondary" sx={{ display: 'block', textAlign: 'right', mt: 1 }}>
                  {msg.timestamp}
                </Typography>
              </Paper>
            </Box>
          </Box>
        ))}
        {isLoading && (
            <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'secondary.main', mr: 2 }}><CoachIcon /></Avatar>
                <Paper variant="outlined" sx={{ p: 2, bgcolor: 'background.paper', borderRadius: '12px' }}>
                    <CircularProgress size={20} />
                </Paper>
            </Box>
        )}
        <div ref={messagesEndRef} />
      </Box>

      {/* Input Area */}
      <Paper component="form" onSubmit={handleSendMessage} sx={{ p: '12px 16px', display: 'flex', alignItems: 'center', borderTop: '1px solid #e0e0e0' }}>
        <TextField
          fullWidth
          variant="standard"
          placeholder="Ask your AI coach..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isLoading}
          InputProps={{ disableUnderline: true }}
          autoFocus
        />
        <IconButton type="submit" color="primary" disabled={!input.trim() || isLoading}>
          <SendIcon />
        </IconButton>
      </Paper>
    </Box>
  );
};

export default CoachChatPage;
