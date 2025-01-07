import { createRoot } from "react-dom/client";
import React, { StrictMode } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage.jsx";
import TableSelectionPage from "./pages/TableSelectionPage.jsx";
import ResultPage from "./pages/ResultPage.jsx";
import ReservationPage from "./pages/ReservationPage.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import RegistrationPage from "./pages/RegistrationPage.jsx";
import ProfilePage from "./pages/ProfilePage.jsx";
import { RequireToken } from "./components/Auth.jsx";
import "./index.css";

createRoot(document.getElementById("root")).render(
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/reservation" element={<ReservationPage />} />
        <Route path="/table_selection" element={<TableSelectionPage />} />
        <Route path="/result" element={<ResultPage />} />
        <Route path="/users/login" element={<LoginPage />} />
        <Route path="/users/register" element={<RegistrationPage />} />
        <Route
          path="/api/v1/users/me"
          element={
            <RequireToken>
              <ProfilePage />
            </RequireToken>
          }
        />
      </Routes>
    </Router>
);