import { useMemo } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";

import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import useMediaQuery from '@mui/material/useMediaQuery';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Badge from '@mui/material/Badge';
import SummarizeIcon from '@mui/icons-material/Summarize';

import './App.css';

import TextSummarizationPage from './components/TextSummarization/TextSummarizationPage';

function App() {
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode: prefersDarkMode ? 'dark' : 'light',
        },
      }),
    [prefersDarkMode],
  );

  return (
    <Router>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar variant="dense">
              <IconButton edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }}>
                <MenuIcon />
              </IconButton>
              <Typography variant="h5" color="inherit" component="div">
                Text Summarization
              </Typography>
              <Box sx={{ flexGrow: 1 }} />
              <IconButton size="large" aria-label="show 4 new mails" color="inherit">
                <Badge badgeContent={4} color="error">
                  <SummarizeIcon />
                </Badge>
              </IconButton>
            </Toolbar>
          </AppBar>
          <Routes>
            <Route path="/" element={<TextSummarizationPage />} />
          </Routes>
        </Box>
      </ThemeProvider>
    </Router>

  );
}

export default App;
