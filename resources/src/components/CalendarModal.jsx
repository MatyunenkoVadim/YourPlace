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

  const today = new Date();
  const maxDate = new Date();
  maxDate.setDate(today.getDate() + 30);

  const todayWithoutTime = new Date(today.getFullYear(), today.getMonth(), today.getDate());

  const calendarDays = [];
  for (let i = 0; i < emptyDays; i++) {
    calendarDays.push(<div className="calendar-day empty" key={`empty-${i}`} />);
  }

  for (let day = 1; day <= daysInMonth; day++) {
    const date = new Date(calendar.year, calendar.month, day);
    const isToday = date.getTime() === todayWithoutTime.getTime();
    const isSelected = selectedDate && date.toDateString() === selectedDate.toDateString();
    const isPast = date < todayWithoutTime;
    const isOutOfRange = date > maxDate;

    calendarDays.push(
      <div
        className={`calendar-day
          ${isToday ? "today" : ""}
          ${isSelected ? "selected" : ""}
          ${isPast || isOutOfRange ? "disabled" : ""}`}
        key={day}
        onClick={() => {
          if (!isPast && !isOutOfRange) {
            setSelectedDate(date);
            onClose();
          }
        }}
      >
        {day}
      </div>
    );
  }

  return calendarDays;
};



  const handlePrevMonth = () => {
  const today = new Date();
  const currentMonth = today.getMonth();
  const currentYear = today.getFullYear();

  if (
    calendar.year > currentYear ||
    (calendar.year === currentYear && calendar.month > currentMonth)
  ) {
    setCalendar((prevState) => ({
      year: prevState.month === 0 ? prevState.year - 1 : prevState.year,
      month: prevState.month === 0 ? 11 : prevState.month - 1,
    }));
  }
};

const handleNextMonth = () => {
  const today = new Date();
  const maxDate = new Date();
  maxDate.setDate(today.getDate() + 30);

  if (
    calendar.year < maxDate.getFullYear() ||
    (calendar.year === maxDate.getFullYear() && calendar.month < maxDate.getMonth())
  ) {
    setCalendar((prevState) => ({
      year: prevState.month === 11 ? prevState.year + 1 : prevState.year,
      month: prevState.month === 11 ? 0 : prevState.month + 1,
    }));
  }
};

const isPrevDisabled = () => {
  const today = new Date();
  const currentMonth = today.getMonth();
  const currentYear = today.getFullYear();

  return calendar.year === currentYear && calendar.month === currentMonth;
};

const isNextDisabled = () => {
  const today = new Date();
  const maxDate = new Date();
  maxDate.setDate(today.getDate() + 30);

  return calendar.year === maxDate.getFullYear() && calendar.month === maxDate.getMonth();
};

  return (
    <div className="calendar-modal">
      <div className="calendar-container">
        <div className="calendar-header">
          <button
            onClick={handlePrevMonth}
            disabled={isPrevDisabled()}
            className={`calendar-nav ${isPrevDisabled() ? "disabled" : ""}`}
          >
            &#8249;
          </button>
          <div className="calendar-month">
            {monthNames[calendar.month]} {calendar.year}
          </div>
          <button
            onClick={handleNextMonth}
            disabled={isNextDisabled()}
            className={`calendar-nav ${isNextDisabled() ? "disabled" : ""}`}
          >
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