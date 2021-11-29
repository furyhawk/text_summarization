import { QueryClient, QueryClientProvider } from "react-query";
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
import useMediaQuery from '@mui/material/useMediaQuery';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import SummarizeIcon from '@mui/icons-material/Summarize';

import './App.css';

// const TextSummarizationPage = lazy(() => import("./components/TextSummarization/TextSummarizationPage"));
import TextSummarizationPage from './components/TextSummarization/TextSummarizationPage';

const queryClient = new QueryClient();

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

  const REACT_APP_VERSION = `${process.env.REACT_APP_NAME} v${process.env.REACT_APP_VERSION}`;

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static">
              <Toolbar variant="dense">
                <SummarizeIcon sx={{ mr: 2 }} />
                <Typography variant="h5" color="inherit" component="div">
                  {REACT_APP_VERSION}
                </Typography>
                <Box sx={{ flexGrow: 1 }} />
              </Toolbar>
            </AppBar>
            <Routes>
              <Route path="/" element={<TextSummarizationPage />} />
            </Routes>
          </Box>
        </ThemeProvider>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
