import React, { useState } from "react";
import axios from "../axiosConfig";
import { useNavigate } from "react-router-dom";
import { fetchToken, setToken } from "../components/Auth.jsx";

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
      const params = new URLSearchParams();
      params.append("username", email);
      params.append("password", password);
      const response = await axios.post("/api/v1/auth/login", params, {
          headers: {
              "Content-Type": "application/x-www-form-urlencoded",
          },
      });
      if (response.data.access_token) {
          setToken(response.data.access_token);
          navigate("/api/v1/users/me");
      }
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
