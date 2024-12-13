import React, { useState } from "react";
import axios from "../axiosConfig";
import { useNavigate } from "react-router-dom";

const RegistrationPage = () => {
  const [username, setUsername] = useState("");
  const [phone, setPhone] = useState("+7");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
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

  const handleRegister = async (e) => {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError("Пароли не совпадают.");
      return;
    }

    try {
      await axios.post("/users/register", {
        username,
        phone: phone.replace(/\D/g, ""),
        password,
      });

      navigate("/");
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
              Имя пользователя
            </label>
          </div>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <div className="label-wrapper">
            <label htmlFor="phone" className="floating-label">
              Телефон
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