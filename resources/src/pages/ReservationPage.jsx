import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header.jsx";
import CalendarModal from "../components/CalendarModal.jsx";
import TimeModal from "../components/TimeModal.jsx";
import GuestsModal from "../components/GuestsModal.jsx";

const getGuestLabel = (count) => {
  if (count === 1) return "гость";
  if (count >= 2 && count <= 4) return "гостя";
  return "гостей";
};

const ReservationPage = () => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [selectedTime, setSelectedTime] = useState("");
  const [guestCount, setGuestCount] = useState(null);
  const [isCalendarOpen, setIsCalendarOpen] = useState(false);
  const [isTimeModalOpen, setIsTimeModalOpen] = useState(false);
  const [isGuestsModalOpen, setIsGuestsModalOpen] = useState(false);

  const navigate = useNavigate();

  const handleOpenCalendar = () => {
    setIsCalendarOpen(true);
  };

  const handleCloseCalendar = () => {
    setIsCalendarOpen(false);
  };

  const handleOpenTimeModal = () => {
    setIsTimeModalOpen(true);
  };

  const handleCloseTimeModal = () => {
    setIsTimeModalOpen(false);
  };

  const handleOpenGuestsModal = () => {
    setIsGuestsModalOpen(true);
  };

  const handleCloseGuestsModal = () => {
    setIsGuestsModalOpen(false);
  };

  const formatDate = (date) => {
    const options = { year: "numeric", month: "long", day: "numeric" };
    return date.toLocaleDateString("ru-RU", options);
  };

  const handleNextClick = () => {
    if (guestCount && selectedTime && selectedDate) {
      const dateParam = encodeURIComponent(selectedDate.toISOString());
      navigate(
        `/table_selection?guest_count=${guestCount}&reservation_date=${dateParam}&reservation_time=${selectedTime}`
      );
    } else {
      alert("Пожалуйста, заполните все поля перед переходом к выбору стола.");
    }
  };

  return (
    <div>
      <Header />
      <div className="content">
        <h1>Забронировать столик</h1>
        <button className="button-info" onClick={handleOpenCalendar}>
          <span className="button-info-content">{formatDate(selectedDate)}</span>
        </button>
        <button className="button-info" onClick={handleOpenTimeModal}>
          <span className="button-info-content">
            {selectedTime || "Выберите время"}
          </span>
        </button>
        <button className="button-info" onClick={handleOpenGuestsModal}>
          <span className="button-info-content">
            {guestCount
              ? `${guestCount} ${getGuestLabel(guestCount)}`
              : "Выберите количество гостей"}
          </span>
        </button>
      </div>

      {/* Кнопка "Перейти к выбору стола" */}
      <div className="next-button-container">
        <button
          className="button"
          onClick={handleNextClick}
          disabled={!guestCount || !selectedTime || !selectedDate}
        >
          Перейти к выбору стола
        </button>
      </div>

      {isCalendarOpen && (
        <CalendarModal
          selectedDate={selectedDate}
          setSelectedDate={setSelectedDate}
          onClose={handleCloseCalendar}
        />
      )}
      {isTimeModalOpen && (
        <TimeModal
          selectedTime={selectedTime}
          setSelectedTime={setSelectedTime}
          onClose={handleCloseTimeModal}
        />
      )}
      {isGuestsModalOpen && (
        <GuestsModal
          guestCount={guestCount}
          setGuestCount={setGuestCount}
          onClose={handleCloseGuestsModal}
        />
      )}
    </div>
  );
};

export default ReservationPage;