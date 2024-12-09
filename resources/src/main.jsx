import { createRoot } from "react-dom/client";
import React, { StrictMode } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage.jsx";
import TableSelectionPage from "./pages/TableSelectionPage.jsx";
import ResultPage from "./pages/ResultPage.jsx";
import ReservationPage from "./pages/ReservationPage.jsx";
import "./index.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/reservation" element={<ReservationPage />} />
        <Route path="/table_selection" element={<TableSelectionPage />} />
        <Route path="/result" element={<ResultPage />} />
      </Routes>
    </Router>
  </StrictMode>
);