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
            {/* <ul>
              <li> */}
                <Link to="/textSummarization" className=''>
                  <span>Text Summarization</span>
                </Link>
              {/* </li>
            </ul> */}
          </nav>
        </header>
        <Routes>
          <Route path="/textSummarization" element={<TextSummarizationPage />} />
        </Routes>
      </div>
    </Router>

  );
}

export default App;
