import React from "react";
import { Link } from "react-router-dom";
import Header from "../components/Header.jsx";

const HomePage = () => {
  return (
    <div>
      <Header />
      <div className="content">
        <h1>Привет, коллега! Мы с Данечком тут че-то натворили, посмотри!</h1>
        <a href="/reservation" className="button">Забронировать столик</a>
      </div>
    </div>
  );
};

export default HomePage;