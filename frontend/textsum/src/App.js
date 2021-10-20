import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";

import './App.css';

import TextSummarizationPage from './components/TextSummarization/TextSummarizationPage';

function App() {

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <nav>
            <Link to="/textSummarization" className=''>
              <span>Text Summarization</span>
            </Link>
          </nav>
        </header>
        <Routes>
          <Route path="/" element={<TextSummarizationPage />} />
          <Route path="/textSummarization" element={<TextSummarizationPage />} />
        </Routes>
      </div>
    </Router>

  );
}

export default App;
