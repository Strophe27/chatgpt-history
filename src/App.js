import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Conversations from "./pages/Conversations";
import ConversationDetail from "./pages/ConversationDetail";


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Conversations />} />
        <Route path="/conversation/:id" element={<ConversationDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
