import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";

const CalendarModal = ({ selectedDate, setSelectedDate, onClose }) => {
  const [calendar, setCalendar] = useState({ year: selectedDate.getFullYear(), month: selectedDate.getMonth() });
  const [weekdays] = useState(["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]);

  const monthNames = [
    "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
  ];

  const createCalendarDays = () => {
    const daysInMonth = new Date(calendar.year, calendar.month + 1, 0).getDate();
    const firstDay = new Date(calendar.year, calendar.month, 1).getDay();
    const emptyDays = (firstDay === 0 ? 6 : firstDay - 1); 

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
          onClick={() => {
            setSelectedDate(date);
            onClose();
          }}
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

  return (
    <div className="calendar-modal">
      <div className="calendar-container">
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
    </div>
  );
};

CalendarModal.propTypes = {
  selectedDate: PropTypes.instanceOf(Date).isRequired,
  setSelectedDate: PropTypes.func.isRequired,
  onClose: PropTypes.func.isRequired,
};

export default CalendarModal;