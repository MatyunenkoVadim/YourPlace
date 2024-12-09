import React from "react";

const TimeModal = ({ selectedTime, setSelectedTime, onClose }) => {
  const times = Array.from({ length: 24 }, (_, i) => i)
    .flatMap((hour) => [
      `${hour.toString().padStart(2, "0")}:00`,
      `${hour.toString().padStart(2, "0")}:30`,
    ])
    .slice(20);

  const handleTimeSelect = (time) => {
    setSelectedTime(time);
    onClose();
  };

  const hours = times.filter((time) => time.endsWith(":00"));
  const halfHours = times.filter((time) => time.endsWith(":30"));

  return (
    <div className="time-modal-overlay" onClick={onClose}>
      <div className="time-modal-container" onClick={(e) => e.stopPropagation()}>
        <h2>Выберите время</h2>
        <div className="time-columns">
          <div className="time-column">
            {hours.map((time) => (
              <div
                key={time}
                className={`time-option ${
                  selectedTime === time ? "selected" : ""
                }`}
                onClick={() => handleTimeSelect(time)}
              >
                {time}
              </div>
            ))}
          </div>
          <div className="time-column">
            {halfHours.map((time) => (
              <div
                key={time}
                className={`time-option ${
                  selectedTime === time ? "selected" : ""
                }`}
                onClick={() => handleTimeSelect(time)}
              >
                {time}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TimeModal;