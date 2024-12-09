import React, { useState, useEffect } from "react";

const Calendar = ({ selectedDate, setSelectedDate }) => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [daysInMonth, setDaysInMonth] = useState([]);

  useEffect(() => {
    const days = createCalendar(currentDate.getFullYear(), currentDate.getMonth());
    setDaysInMonth(days);
  }, [currentDate]);

  const createCalendar = (year, month) => {
    const firstDay = new Date(year, month, 1).getDay();
    const lastDateOfMonth = new Date(year, month + 1, 0).getDate();
    const daysArray = [];

    // Add empty cells for the previous month
    for (let i = 0; i < (firstDay || 7) - 1; i++) {
      daysArray.push(null);
    }

    // Add days for the current month
    for (let i = 1; i <= lastDateOfMonth; i++) {
      daysArray.push(i);
    }

    return daysArray;
  };

  const handlePrevMonth = () => {
    setCurrentDate(new Date(currentDate.setMonth(currentDate.getMonth() - 1)));
  };

  const handleNextMonth = () => {
    setCurrentDate(new Date(currentDate.setMonth(currentDate.getMonth() + 1)));
  };

  const handleDayClick = (day) => {
    if (day !== null) {
      const newDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), day);
      setSelectedDate(newDate);
    }
  };

  const renderCalendar = () => {
    const daysOfWeek = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"];
    const monthNames = [
      "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль",
      "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ];

    const firstDay = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay();
    const monthName = monthNames[currentDate.getMonth()];
    const year = currentDate.getFullYear();

    return (
      <div className="calendar">
        <div className="calendar-header">
          <button onClick={handlePrevMonth}>&#8249;</button>
          <span>{`${monthName} ${year}`}</span>
          <button onClick={handleNextMonth}>&#8250;</button>
        </div>
        <div className="calendar-weekdays">
          {daysOfWeek.map((day, index) => (
            <div key={index} className="calendar-weekday">{day}</div>
          ))}
        </div>
        <div className="calendar-days">
          {daysInMonth.map((day, index) => (
            <div
              key={index}
              className={`calendar-day ${day === null ? "empty" : ""} ${selectedDate?.getDate() === day ? "selected" : ""}`}
              onClick={() => handleDayClick(day)}
            >
              {day}
            </div>
          ))}
        </div>
      </div>
    );
  };

  return <div>{renderCalendar()}</div>;
};

export default Calendar;