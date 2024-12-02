import { createRoot } from "react-dom/client";
import React, { StrictMode } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage.jsx";
import GuestsPage from "./pages/GuestsPage.jsx";
import DatetimePage from "./pages/DatetimePage.jsx";
import TableSelectionPage from "./pages/TableSelectionPage.jsx";
import ResultPage from "./pages/ResultPage.jsx";
import "./index.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/guests" element={<GuestsPage />} />
        <Route path="/datetime" element={<DatetimePage />} />
        <Route path="/table_selection" element={<TableSelectionPage />} />
        <Route path="/result" element={<ResultPage />} />
      </Routes>
    </Router>
  </StrictMode>
);