import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Header from "../components/Header.jsx";

const DatetimePage = () => {
  const [selectedDate, setSelectedDate] = useState(null);
  const [calendar, setCalendar] = useState({ year: new Date().getFullYear(), month: new Date().getMonth() });
  const [timeSelection, setTimeSelection] = useState("");
  const [guestCount, setGuestCount] = useState(null);
  const navigate = useNavigate();

  const monthNames = [
    "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
  ];

  const weekdays = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"];

  const location = useLocation();
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const count = params.get("guest_count");
    if (count) {
      setGuestCount(count);
    }
  }, [location]);

  const createCalendarDays = () => {
    const daysInMonth = new Date(calendar.year, calendar.month + 1, 0).getDate();
    const firstDay = new Date(calendar.year, calendar.month, 1).getDay();
    const emptyDays = (firstDay === 0 ? 6 : firstDay - 1); // Понедельник как первый день недели

    const calendarDays = [];
    for (let i = 0; i < emptyDays; i++) {
      calendarDays.push(<div className="calendar-day empty" key={`empty-${i}`} />);
    }

    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(calendar.year, calendar.month, day);
      const isToday = date.toDateString() === new Date().toDateString();
      const isSelected = selectedDate && date.toDateString() === selectedDate.toDateString();

      calendarDays.push(
        <div
          className={`calendar-day ${isToday ? "today" : ""} ${isSelected ? "selected" : ""}`}
          key={day}
          onClick={() => setSelectedDate(date)}
        >
          {day}
        </div>
      );
    }

    return calendarDays;
  };

  const handlePrevMonth = () => {
    setCalendar((prevState) => ({
      year: prevState.month === 0 ? prevState.year - 1 : prevState.year,
      month: prevState.month === 0 ? 11 : prevState.month - 1,
    }));
  };

  const handleNextMonth = () => {
    setCalendar((prevState) => ({
      year: prevState.month === 11 ? prevState.year + 1 : prevState.year,
      month: prevState.month === 11 ? 0 : prevState.month + 1,
    }));
  };

  const handleSubmit = () => {
    if (selectedDate && timeSelection) {
      const [hours, minutes] = timeSelection.split(":");
      selectedDate.setHours(hours, minutes);

      const reservationDate = selectedDate.toISOString();
      navigate(`/table_selection?guest_count=${guestCount}&reservation_date=${reservationDate}`);
    } else {
      alert("Пожалуйста, выберите дату и время!");
    }
  };

  return (
    <div>
      <Header />
      <div className="content">
        <h1>Выберите дату и время</h1>
        <div id="calendar" className="calendar-container">
          <div className="calendar-header">
            <button onClick={handlePrevMonth} className="calendar-nav">
              &#8249;
            </button>
            <div className="calendar-month">
              {monthNames[calendar.month]} {calendar.year}
            </div>
            <button onClick={handleNextMonth} className="calendar-nav">
              &#8250;
            </button>
          </div>

          <div className="calendar-days">
            {weekdays.map((day) => (
              <div key={day} className="calendar-weekday">{day}</div>
            ))}
            {createCalendarDays()}
          </div>
        </div>

        <div className="time-selection-container">
          <label htmlFor="time-selection">Выберите время:</label>
          <select
            id="time-selection"
            required
            onChange={(e) => setTimeSelection(e.target.value)}
          >
            <option value="" disabled selected>Выберите время</option>
            <option value="10:00">10:00</option>
            <option value="11:00">11:00</option>
            <option value="12:00">12:00</option>
            <option value="13:00">13:00</option>
            <option value="14:00">14:00</option>
          </select>
        </div>

        <button onClick={handleSubmit} className="button" disabled={!selectedDate || !timeSelection}>
          Продолжить
        </button>
      </div>
    </div>
  );
};

export default DatetimePage;
