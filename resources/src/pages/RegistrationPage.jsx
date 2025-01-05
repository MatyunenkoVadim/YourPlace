import React, { useState } from "react";
import axios from "../axiosConfig";
import { useNavigate } from "react-router-dom";
import { fetchToken, setToken } from "../components/Auth.jsx";

const RegistrationPage = () => {
  const [email, setEmail] = useState("");
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
      const responseReg = await axios.post("/api/v1/auth/register", {
        email,
        password,
      });
      if (responseReg.data) {
          const params = new URLSearchParams();
          params.append("username", email);
          params.append("password", password);
          const responseLog = await axios.post("/api/v1/auth/login", params, {
              headers: {
                "Content-Type": "application/x-www-form-urlencoded",
              },
          });
          console.log(username, "username");
          console.log(responseLog.data, "response");
          setToken(responseLog.data.access_token);
          console.log(responseLog.data.access_token);
          navigate("/api/v1/users/me");
      }
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
            <label htmlFor="email" className="floating-label">
              Имя пользователя (Email)
            </label>
          </div>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
