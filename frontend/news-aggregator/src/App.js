import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NewsFeed from "./components/NewsFeed";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<NewsFeed />} />
            </Routes>
        </Router>
    );
}

export default App;
