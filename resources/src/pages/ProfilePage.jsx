import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import axios from "../axiosConfig";
import Header from "../components/Header";

export default function ProfilePage() {
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      const auth = localStorage.getItem("temitope");
      try {
        const response = await axios.get("/api/v1/users/me", {
          headers: {
            Authorization: `Bearer ${auth}`,
          },
        });
        setUserData(response.data);
      } catch (err) {
        setError("Failed to load user data");
      }
    };
    fetchUserData();
  }, []);

  const signOut = () => {
    localStorage.removeItem("temitope");
    navigate("/");
  };

  return (
    <div>
      <Header />
      <div className="profile-container">
        <div className="profile-info">
          <h1 className="profile-title">Мой профиль</h1>
          {error ? (
            <p style={{ color: "red" }}>{error}</p>
          ) : userData ? (
            <>
              <div className="profile-data">
                <p className="profile-name">{userData.name}Пример текста</p>
              </div>
              <div className="profile-data">
                <p className="profile-email">{userData.email}Пример текста</p>
              </div>
              <div className="profile-data">
                <p className="profile-phone">{userData.phone}Пример текста</p>
              </div>
            </>
          ) : (
            <p>Loading...</p>
          )}
        </div>
        <div className="profile-image">
          {userData && userData.image ? (
            <img src={userData.image} alt="Profile" className="profile-pic" />
          ) : (
            <div className="default-profile-pic"></div>
          )}
        </div>
      </div>
      <button onClick={signOut} className="sign-out-button">Выйти</button>
    </div>
  );
}
