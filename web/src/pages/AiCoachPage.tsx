import React, { useState, useEffect, useRef } from 'react';
import { Box, TextField, Button, Paper, Typography, List, ListItem, Avatar, CircularProgress, IconButton, Accordion, AccordionSummary, AccordionDetails, Snackbar } from '@mui/material';
import { styled, useTheme } from '@mui/material/styles';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import PersonIcon from '@mui/icons-material/Person';
import SendIcon from '@mui/icons-material/Send';
import ReplayIcon from '@mui/icons-material/Replay';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import BugReportIcon from '@mui/icons-material/BugReport';

const ChatContainer = styled(Paper)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  height: 'calc(100vh - 120px)',
  maxWidth: '900px',
  margin: '16px auto',
  borderRadius: '12px',
  boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
}));

const MessagesContainer = styled(Box)({
  flexGrow: 1,
  overflowY: 'auto',
  padding: '16px 24px',
});

const InputContainer = styled(Box)(({ theme }) => ({
  padding: '16px 24px',
  borderTop: `1px solid ${theme.palette.divider}`,
  backgroundColor: theme.palette.background.default,
  display: 'flex',
  alignItems: 'center',
}));

interface Message {
  id: number;
  role: 'user' | 'assistant' | 'system';
  content: string;
  error?: boolean;
}

const systemPrompt: Message = {
  id: 0,
  role: 'system',
  content: 'You are a friendly and expert chess coach. Provide clear, encouraging advice. Explain concepts simply. If asked about non-chess topics, politely decline and steer the conversation back to chess.',
};

interface DebugInfo {
  lastPayload: object | null;
  lastResponse: string | object | null;
  lastError: object | null;
  status: 'idle' | 'sending' | 'success' | 'error';
}

const AiCoachPage: React.FC = () => {
  const theme = useTheme();
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, role: 'assistant', content: 'Hi there! I\'m your AI chess coach. Ask me anything about openings, tactics, or strategy!' },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const [showSendingToast, setShowSendingToast] = useState(false);
  const [debugInfo, setDebugInfo] = useState<DebugInfo>({
    lastPayload: null,
    lastResponse: null,
    lastError: null,
    status: 'idle',
  });

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (messageToRetry?: Message) => {
    const isRetry = !!messageToRetry;
    const content = isRetry ? messageToRetry!.content : input.trim();

    if (!content || (isLoading && !isRetry)) return;
    
    if (isRetry) {
      console.log(`[AI Coach] Retrying message: "${content}"`);
    } else {
      console.log(`[AI Coach] Attempting to send: "${content}"`);
    }

    setIsLoading(true);
    setShowSendingToast(true);
    const userMessage: Message = isRetry ? { ...messageToRetry, error: false } : { id: Date.now(), role: 'user', content };

    if (!isRetry) {
      setInput('');
    }

    setMessages(prevMessages => {
      const newMessages = isRetry
        ? prevMessages.map(m => (m.id === userMessage.id ? userMessage : m))
        : [...prevMessages, userMessage];

      const conversationHistory = [systemPrompt, ...newMessages]
        .filter(m => !m.error)
        .map(({ role, content }) => ({ role, content }));
      
      const payload = { messages: conversationHistory };
      setDebugInfo({ lastPayload: payload, lastResponse: null, lastError: null, status: 'sending' });
      console.log('[AI Coach] Sending payload:', JSON.stringify(payload, null, 2));

      (async () => {
        try {
          const response = await fetch('http://localhost:8000/api/coach/stream_ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
          });

          if (!response.ok || !response.body) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
          }
          
          console.log('[AI Coach] Received successful response stream.');
          setDebugInfo(prev => ({ ...prev, status: 'success' }));

          const reader = response.body.getReader();
          const decoder = new TextDecoder();
          let aiResponse = '';
          const aiMessageId = Date.now() + 1;

          setMessages(prev => [...prev, { id: aiMessageId, role: 'assistant', content: '' }]);

          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            aiResponse += decoder.decode(value, { stream: true });
            setMessages(prev =>
              prev.map(msg => (msg.id === aiMessageId ? { ...msg, content: aiResponse + '...' } : msg))
            );
          }

          setMessages(prev =>
            prev.map(msg => (msg.id === aiMessageId ? { ...msg, content: aiResponse } : msg))
          );
          setDebugInfo(prev => ({ ...prev, lastResponse: aiResponse }));

        } catch (error: any) {
          console.error('[AI Coach] Send error:', error);
          setDebugInfo(prev => ({ ...prev, lastError: { message: error.message, stack: error.stack }, status: 'error' }));
          setMessages(prev =>
            prev.map(m => (m.id === userMessage.id ? { ...m, error: true } : m))
          );
        } finally {
          setIsLoading(false);
          setShowSendingToast(false);
        }
      })();

      return newMessages;
    });
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const renderMessage = (msg: Message) => {
    if (msg.role === 'system') return null;

    const isUser = msg.role === 'user';
    const alignment = isUser ? 'flex-end' : 'flex-start';
    const avatar = isUser ? <PersonIcon /> : <SmartToyIcon />;
    const bgColor = isUser ? theme.palette.secondary.main : theme.palette.primary.main;

    return (
      <ListItem key={msg.id} sx={{ display: 'flex', justifyContent: alignment, mb: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2, maxWidth: '85%' }}>
          {!isUser && <Avatar sx={{ bgcolor: 'primary.main' }}>{avatar}</Avatar>}
          <Paper
            elevation={2}
            sx={{
              p: '12px 16px',
              borderRadius: '12px',
              bgcolor: msg.error ? theme.palette.error.light : bgColor,
              color: 'white',
              whiteSpace: 'pre-wrap',
            }}
          >
            <Typography variant="body1">{msg.content}</Typography>
            {msg.error && (
              <Button
                size="small"
                variant="text"
                onClick={() => handleSendMessage(msg)}
                sx={{ color: 'white', mt: 1, textTransform: 'none' }}
                startIcon={<ReplayIcon />}
              >
                Retry
              </Button>
            )}
          </Paper>
          {isUser && <Avatar sx={{ bgcolor: 'grey.500' }}>{avatar}</Avatar>}
        </Box>
      </ListItem>
    );
  };

  return (
    <Box>
      <Snackbar
        open={showSendingToast}
        message="Sending to AI Coach..."
        key={'sending-toast'}
      />
      <ChatContainer elevation={3}>
      <MessagesContainer>
        <List>
          {messages.map((msg) => renderMessage(msg))}
          {isLoading && !messages.some(m => m.role === 'assistant' && m.content.endsWith('...')) && (
              <ListItem sx={{ display: 'flex', justifyContent: 'flex-start', mb: 2 }}>
                  <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}><SmartToyIcon /></Avatar>
                  <CircularProgress size={24} />
              </ListItem>
          )}
          <div ref={messagesEndRef} />
        </List>
      </MessagesContainer>
      <InputContainer>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Ask your AI coach..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          sx={{ '& .MuiOutlinedInput-root': { borderRadius: '30px' } }}
        />
        <IconButton color="primary" onClick={() => handleSendMessage()} disabled={isLoading} sx={{ ml: 1, bgcolor: 'primary.main', color: 'white', '&:hover': { bgcolor: 'primary.dark' } }}>
          <SendIcon />
        </IconButton>
      </InputContainer>
    </ChatContainer>
    <DebugPanel info={debugInfo} />
    </Box>
  );
};

const DebugPanel: React.FC<{ info: DebugInfo }> = ({ info }) => {
  const theme = useTheme();
  return (
    <Accordion sx={{ maxWidth: '900px', margin: '0 auto', mt: 1 }}>
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <BugReportIcon sx={{ mr: 1 }} />
        <Typography>Debug Panel</Typography>
      </AccordionSummary>
      <AccordionDetails sx={{ backgroundColor: theme.palette.grey[100], maxHeight: 300, overflowY: 'auto' }}>
        <Box>
          <Typography variant="subtitle2">Status: {info.status}</Typography>
          <Typography variant="subtitle2" sx={{ mt: 1 }}>Last Payload:</Typography>
          <Paper component="pre" sx={{ p: 1, whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>
            {JSON.stringify(info.lastPayload, null, 2) || 'null'}
          </Paper>
          <Typography variant="subtitle2" sx={{ mt: 1 }}>Last Response:</Typography>
          <Paper component="pre" sx={{ p: 1, whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>
            {info.lastResponse ? JSON.stringify(info.lastResponse, null, 2) : 'null'}
          </Paper>
          <Typography variant="subtitle2" sx={{ mt: 1 }}>Last Error:</Typography>
          <Paper component="pre" sx={{ p: 1, whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>
            {info.lastError ? JSON.stringify(info.lastError, null, 2) : 'null'}
          </Paper>
        </Box>
      </AccordionDetails>
    </Accordion>
  );
};

export default AiCoachPage;

