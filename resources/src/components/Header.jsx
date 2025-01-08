import React, { useState } from "react";
import "../index.css";
import Logo from "../images/logo.svg";

const Header = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <header className="header">
      <div className="header-logo">
        <img src={Logo} alt="Своё Место" className="logo" />
      </div>

      <button className="menu-toggle" onClick={toggleMenu}>
        ☰
      </button>

      <nav className={`nav-links ${menuOpen ? "nav-open" : ""}`}>
        <a href="/" className="nav-link">Главная</a>
        <a href="/reservations" className="nav-link">Мои бронирования</a>
        <a href="/contacts" className="nav-link">Контакты</a>
        <a href="/users/login" className="nav-link mobile-login-button">Войти</a>
      </nav>

      <a href="/users/login" className="log-button">Войти</a>
    </header>
  );
};

export default Header;
