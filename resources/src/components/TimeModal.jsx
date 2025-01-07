import React from "react";

const TimeModal = ({ selectedTime, setSelectedTime, onClose, selectedDate }) => {
  const now = new Date();

  const times = Array.from({ length: 13 }, (_, i) => i + 10)
  .flatMap((hour) => [
    `${hour.toString().padStart(2, "0")}:00`,
    `${hour.toString().padStart(2, "0")}:30`,
  ]);

  const isToday = selectedDate
    ? selectedDate.toDateString() === now.toDateString()
    : false;

  const isTimeDisabled = (time) => {
    if (!isToday) return false;

    const [hour, minute] = time.split(":").map(Number);
    const currentHour = now.getHours();
    const currentMinute = now.getMinutes();

    return hour < currentHour || (hour === currentHour && minute <= currentMinute);
  };

  const handleTimeSelect = (time) => {
    if (!isTimeDisabled(time)) {
      const timeParts = time.split(":");
      const formattedTime = `${timeParts[0].padStart(2, "0")}:${timeParts[1].padStart(2, "0")}`;
      setSelectedTime(formattedTime);
      onClose();
    }
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
                } ${isTimeDisabled(time) ? "disabled" : ""}`}
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
                } ${isTimeDisabled(time) ? "disabled" : ""}`}
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
