import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import axios from "../axiosConfig";

export default function ProfilePage() {
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      const auth = localStorage.getItem("temitope");
      try {
        const response = await axios.get("http://localhost:8000/api/v1/auth/register", {
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
    <>
      <div style={{ marginTop: 20, minHeight: 700 }}>
        <h1>Profile page</h1>
        {error ? (
          <p style={{ color: "red" }}>{error}</p>
        ) : userData ? (
          <>
            <p>Hello {userData.name}, welcome to your profile page</p>
            <p>Email: {userData.email}</p>
          </>
        ) : (
          <p>Loading...</p>
        )}

        <button onClick={signOut}>sign out</button>
      </div>
    </>
  );
}
