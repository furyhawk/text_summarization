import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";

import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';

import './App.css';

import TextSummarizationPage from './components/TextSummarization/TextSummarizationPage';

function App() {

  return (
    <Router>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar variant="dense">
            <IconButton edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }}>
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" color="inherit" component="div">
              Text Summarization
            </Typography>
          </Toolbar>
        </AppBar>
        <Routes>
          <Route path="/" element={<TextSummarizationPage />} />
          <Route path="/textSummarization" element={<TextSummarizationPage />} />
        </Routes>
      </Box>
    </Router>

  );
}

export default App;
