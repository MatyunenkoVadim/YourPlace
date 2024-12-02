import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header.jsx";

const GuestsPage = () => {
  const [guestCount, setGuestCount] = useState(null);
  const navigate = useNavigate();

  const handleGuestSelect = (count) => {
    setGuestCount(count);
  };

  const handleNextClick = () => {
    if (guestCount) {
      navigate(`/datetime?guest_count=${guestCount}`);
    }
  };

  return (
    <div>
      <Header />
      <div className="content">
        <h1>Выберите кол-во гостей</h1>
        <div className="guest-count-container">
          {[1, 2, 3, 4, 5, 6].map((count) => (
            <div
              key={count}
              className={`guest-option ${guestCount === count ? "selected" : ""}`}
              onClick={() => handleGuestSelect(count)}
            >
              {count}
            </div>
          ))}
        </div>
        <button
          onClick={handleNextClick}
          className="button"
          disabled={!guestCount}
        >
          Дальше
        </button>
      </div>
    </div>
  );
};

export default GuestsPage;