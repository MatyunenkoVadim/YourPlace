import React from "react";
import { Link } from "react-router-dom";
import Header from "../components/Header.jsx";
import backgroundImage from "../images/background.svg";
import logoImage from "../images/white_logo.svg";

const HomePage = () => {
  return (
    <div className="home-container">
      <Header />
      <div
        className="background-image-container"
        style={{
          backgroundImage: `url(${backgroundImage})`,
        }}
      ></div>
      <div className="welcome-text">
        <h1>Добро пожаловать!</h1>
        <div className="welcome-text-paragraphs">
          <p>«Своё место» - сервис для бронирования столиков в ресторане.</p>
          <p>Вы находитесь на тестовом варианте сервиса для ознакомления с функционалом.</p>
          <p>На этой странице будет располагаться информация о вашем заведении.</p>
          <p>Мы поможем вашему ресторану найти «Своё место» в сердцах гостей!</p>
        </div>
        <div className="button-home-container">
          <Link to="/reservation" className="button-home">Начать бронирование</Link>
        </div>
      </div>
      <div className="logo-container">
        <div className="logo-part"
          style={{
            backgroundImage: `url(${logoImage})`,
          }}
        ></div>
      </div>
    </div>
  );
};

export default HomePage;
