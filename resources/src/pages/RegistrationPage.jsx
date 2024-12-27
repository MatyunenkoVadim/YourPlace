import React, { useState } from "react";
import axios from "../axiosConfig";
import { useNavigate } from "react-router-dom";
import { fetchToken, setToken } from "../components/Auth.jsx";

const RegistrationPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError("Пароли не совпадают.");
      return;
    }

    try {
      const response = await axios.post("http://localhost:8000/api/v1/auth/register", {
        username: email,
        password,
      })
      .then(function (response) {
          console.log(response.data.token, "response.data.token");
          if (response.data.token) {
            setToken(response.data.token);
            navigate("/users/me");
          }
      });
    } catch (err) {
      if (err.response && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError("Ошибка регистрации. Попробуйте снова.");
      }
    }
  };

  return (
    <div className="login-page">
      <h1 className="login-title">Регистрация</h1>

      <form className="login-form" onSubmit={handleRegister}>
        <div className="form-group">
          <div className="label-wrapper">
            <label htmlFor="username" className="floating-label">
              Имя пользователя (Email)
            </label>
          </div>
          <input
            type="email"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
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

        <div className="form-group">
          <div className="label-wrapper">
            <label htmlFor="confirm_password" className="floating-label">
              Подтвердите пароль
            </label>
          </div>
          <input
            type="password"
            id="confirm_password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>

        {error && <p className="error-message">{error}</p>}

        <button type="submit" className="login-button">
          Зарегистрироваться
        </button>
      </form>
    </div>
  );
};

export default RegistrationPage;
