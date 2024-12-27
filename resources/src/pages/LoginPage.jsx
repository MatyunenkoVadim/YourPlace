import React, { useState } from "react";
import axios from "../axiosConfig";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await axios.post("http://localhost:8000/api/v1/auth/login", {
        username: email,
        password,
      });
    } catch (error) {
      setError("Ошибка входа. Проверьте email или пароль.");
    }
  };

  return (
    <div className="login-page">
      <h1 className="login-title">Вход</h1>

      <form className="login-form" onSubmit={handleLogin}>
        <div className="form-group">
          <div className="label-wrapper">
            <label htmlFor="email" className="floating-label">
              Email
            </label>
          </div>
          <input
            type="email"
            id="email"
            value={email}
            onChange={handleEmailChange}
            required
          />
        </div>

        <div className="form-group">
          <div className="label-wrapper">
            <label htmlFor="password" className="floating-label">
              Пароль
            </label>
          </div>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {error && <p className="error-message">{error}</p>}

        <button type="submit" className="login-button">
          Войти
        </button>
      </form>

      <div className="register-link">
        <p>Еще нет аккаунта?</p>
        <a href="/users/register" className="register-button">
          Зарегистрироваться
        </a>
      </div>
    </div>
  );
};

export default LoginPage;
