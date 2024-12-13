import React, { useState } from "react";
import axios from "../axiosConfig";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const [phone, setPhone] = useState("+7");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const MAX_LENGTH = 10;

  const handlePhoneChange = (e) => {
    const value = e.target.value;

    const digits = value.replace(/\D/g, "").slice(1);
    if (digits.length <= MAX_LENGTH) {
      setPhone("+7" + digits);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await axios.post("http://localhost:8000/users/login", {
        username: phone.replace(/\D/g, ""),
        password,
      });
      const { access_token } = response.data;

      localStorage.setItem("access_token", access_token);

      navigate("/");
    } catch (error) {
      setError("Ошибка входа. Проверьте телефон или пароль.");
    }
  };

  return (
    <div className="login-page">
      <h1 className="login-title">Вход</h1>

      <form className="login-form" onSubmit={handleLogin}>
        <div className="form-group">
          <div className="label-wrapper">
            <label htmlFor="phone" className="floating-label">
              Номер телефона
            </label>
          </div>
          <input
            type="tel"
            id="phone"
            value={phone}
            onChange={handlePhoneChange}
            required
            maxLength="13"
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