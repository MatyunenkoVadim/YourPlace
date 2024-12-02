import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import seatingImage from '../images/seating.svg';
import tableFor4 from '../images/tableFor4.svg';
import tableFor4Selected from '../images/tableFor4_selected.svg';
import tableFor6 from '../images/tableFor6.svg';
import tableFor6Selected from '../images/tableFor6_selected.svg';
import tableFor2 from '../images/tableFor2.svg';
import tableFor2Selected from '../images/tableFor2_selected.svg';
import tableFor5 from '../images/tableFor5.svg';
import tableFor5Selected from '../images/tableFor5_selected.svg';
import Header from "../components/Header.jsx";

const TableSelectionPage = () => {
  const [selectedTable, setSelectedTable] = useState(null);
  const [hoveredTable, setHoveredTable] = useState(null);
  const [guestCount, setGuestCount] = useState(null);
  const [reservationDate, setReservationDate] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const count = params.get("guest_count");
    const date = params.get("reservation_date");
    if (count && date) {
      setGuestCount(count);
      setReservationDate(date);
    } else {
      navigate("/datetime");
    }
  }, [location, navigate]);

  const selectTable = (tableId) => {
    setSelectedTable(tableId);
  };

  const tableCoordinates = [
    { id: 1, image: tableFor4, imageSelected: tableFor4Selected, style: { top: '10%', left: '16.5%', width: '12%', height: '12%' } },
    { id: 2, image: tableFor4, imageSelected: tableFor4Selected, style: { top: '10%', left: '32.5%', width: '12%', height: '12%' } },
    { id: 3, image: tableFor6, imageSelected: tableFor6Selected, style: { top: '14%', left: '80%' } },
    { id: 4, image: tableFor6, imageSelected: tableFor6Selected, style: { top: '24%', left: '3%', transform: 'rotate(90deg)' } },
    { id: 5, image: tableFor6, imageSelected: tableFor6Selected, style: { top: '24%', left: '16.5%', transform: 'rotate(90deg)' } },
    { id: 6, image: tableFor4, imageSelected: tableFor4Selected, style: { top: '51%', left: '71%' } },
    { id: 7, image: tableFor2, imageSelected: tableFor2Selected, style: { top: '62%', left: '8%' } },
    { id: 8, image: tableFor2, imageSelected: tableFor2Selected, style: { top: '62%', left: '19%' } },
    { id: 9, image: tableFor2, imageSelected: tableFor2Selected, style: { top: '60%', left: '27%', transform: 'rotate(90deg)' } },
    { id: 10, image: tableFor2, imageSelected: tableFor2Selected, style: { top: '60%', left: '54%', transform: 'rotate(90deg)' } },
    { id: 11, image: tableFor5, imageSelected: tableFor5Selected, style: { top: '89%', left: '10%', width: '12%', height: '12%' } },
    { id: 12, image: tableFor5, imageSelected: tableFor5Selected, style: { top: '89%', left: '21.5%', width: '12%', height: '12%' } },
    { id: 13, image: tableFor5, imageSelected: tableFor5Selected, style: { top: '89%', left: '33%', width: '12%', height: '12%' } },
    { id: 14, image: tableFor5, imageSelected: tableFor5Selected, style: { top: '89%', left: '57.3%', width: '12%', height: '12%' } },
    { id: 15, image: tableFor5, imageSelected: tableFor5Selected, style: { top: '89%', left: '69.5%', width: '12%', height: '12%' } },
    { id: 16, image: tableFor5, imageSelected: tableFor5Selected, style: { top: '89%', left: '82%', width: '12%', height: '12%' } }
  ];

  return (
    <div>
      <Header />
      <h1>Выберите столик</h1>
      <div
        className="seating-layout"
        style={{
          backgroundImage: `url(${seatingImage})`,
          backgroundSize: 'contain',
          backgroundRepeat: 'no-repeat',
          position: 'relative',
          height: '100%',
        }}
      >
        {tableCoordinates.map((table) => {
          const { id, image, imageSelected, style } = table;

          const currentImage =
            selectedTable === id || hoveredTable === id
              ? imageSelected
              : image;

          return (
            <div
              key={id}
              className={`table-point ${selectedTable === id ? 'selected' : ''}`}
              style={style}
              onClick={() => selectTable(id)}
              onMouseEnter={() => setHoveredTable(id)}
              onMouseLeave={() => setHoveredTable(null)}
            >
              <img
                src={currentImage}
                alt={`Table for ${id}`}
                style={{ width: '100%', height: '100%', objectFit: 'contain' }}
              />
            </div>
          );
        })}
      </div>

      <form action="/result" method="post" id="reservationForm" style={{ display: selectedTable ? 'block' : 'none' }}>
        <input type="hidden" name="guest_count" value={guestCount || ''} />
        <input type="hidden" name="reservation_date" value={reservationDate || ''} />
        <input type="hidden" name="table_number" value={selectedTable || ''} />
        <button type="submit" className="button">Забронировать</button>
      </form>
    </div>
  );
};

export default TableSelectionPage;