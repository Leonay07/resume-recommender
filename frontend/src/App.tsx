import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import LandingPage from "./pages/LandingPage";
import JobFeedPage from "./pages/JobFeedPage";
import SearchPage from "./pages/SearchPage";
import ResultPage from "./pages/ResultPage";
import JobDetailPage from "./pages/JobDetailPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/feed" element={<JobFeedPage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/result" element={<ResultPage />} />
        <Route path="/job" element={<JobDetailPage />} />
      </Routes>
    </Router>
  );
}

export default App;
