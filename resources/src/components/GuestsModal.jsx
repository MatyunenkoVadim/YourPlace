import React, { useState } from "react";

const GuestsModal = ({ guestCount, setGuestCount, onClose }) => {
  const handleGuestSelect = (count) => {
    setGuestCount(count);
    onClose();
  };


  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Выберите количество гостей</h2>
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
      </div>
    </div>
  );
};

export default GuestsModal;