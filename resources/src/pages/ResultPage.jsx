import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axiosInstance from "../axiosConfig";
import Header from "../components/Header.jsx";

const ResultPage = () => {
  const [guestCount, setGuestCount] = useState(null);
  const [reservationDate, setReservationDate] = useState(null);
  const [tableNumber, setTableNumber] = useState(null);
  const [loading, setLoading] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const count = params.get("guest_count");
    const date = params.get("reservation_date");
    const table = params.get("table_number");

    if (count && date && table) {
      setGuestCount(count);
      setReservationDate(new Date(date).toLocaleString("ru-RU", {
        day: "numeric",
        month: "long",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      }));
      setTableNumber(table);
    } else {
      navigate("/");
    }
  }, [location, navigate]);

  const handleReservation = async () => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("guest_count", guestCount);
      formData.append("reservation_date", reservationDate);
      formData.append("table_number", tableNumber);

      const response = await axiosInstance.post("/result", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log("Reservation successful:", response.data);
    } catch (error) {
      console.error("Error during reservation:", error);
      alert("Произошла ошибка при бронировании. Пожалуйста, попробуйте снова.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Header />
      <div className="content">
        {guestCount && reservationDate && tableNumber ? (
          <>
            <h1>Бронирование прошло успешно!</h1>
            <p>
              <strong>Кол-во гостей:</strong> {guestCount}
            </p>
            <p>
              <strong>Дата и время:</strong> {reservationDate}
            </p>
            <p>
              <strong>Номер столика:</strong> {tableNumber}
            </p>
            <button onClick={handleReservation} disabled={loading} className="button">
              {loading ? "Бронирование..." : "Забронировать"}
            </button>
            <a href="/" className="button">
              Вернуться на главную
            </a>
          </>
        ) : (
          <p>Загрузка информации о бронировании...</p>
        )}
      </div>
    </div>
  );
};

export default ResultPage;
