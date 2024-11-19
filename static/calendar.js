document.addEventListener("DOMContentLoaded", () => {
    const calendarContainer = document.getElementById("calendar");
    const reservationDateInput = document.getElementById("reservation_date");
    const timeSelection = document.getElementById("time-selection");
    const form = document.querySelector("form");

    const today = new Date();
    let selectedDate = null;

    function createCalendar(year, month) {
        // Корректируем месяц и год
        const correctedDate = new Date(year, month);
        year = correctedDate.getFullYear();
        month = correctedDate.getMonth();

        calendarContainer.innerHTML = "";

        const monthNames = [
            "Январь", "Февраль", "Март", "Апрель",
            "Май", "Июнь", "Июль", "Август",
            "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ];

        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const firstDay = new Date(year, month, 1).getDay();

        const header = document.createElement("div");
        header.className = "calendar-header";

        const prevButton = document.createElement("button");
        prevButton.innerHTML = "&#8249;";
        prevButton.className = "calendar-nav";
        prevButton.onclick = (e) => {
            e.preventDefault();
            createCalendar(year, month - 1);
        };

        const nextButton = document.createElement("button");
        nextButton.innerHTML = "&#8250;";
        nextButton.className = "calendar-nav";
        nextButton.onclick = (e) => {
            e.preventDefault();
            createCalendar(year, month + 1);
        };

        const monthTitle = document.createElement("div");
        monthTitle.className = "calendar-month";
        monthTitle.textContent = `${monthNames[month]} ${year}`;

        header.appendChild(prevButton);
        header.appendChild(monthTitle);
        header.appendChild(nextButton);
        calendarContainer.appendChild(header);

        const daysContainer = document.createElement("div");
        daysContainer.className = "calendar-days";

        const weekdays = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"];
        weekdays.forEach(day => {
            const weekday = document.createElement("div");
            weekday.className = "calendar-weekday";
            weekday.textContent = day;
            daysContainer.appendChild(weekday);
        });

        for (let i = 0; i < (firstDay || 7) - 1; i++) { // Смещение для понедельника как первого дня
            const emptyCell = document.createElement("div");
            emptyCell.className = "calendar-day empty";
            daysContainer.appendChild(emptyCell);
        }

        for (let day = 1; day <= daysInMonth; day++) {
            const dayCell = document.createElement("div");
            dayCell.className = "calendar-day";
            dayCell.textContent = day;

            const date = new Date(year, month, day);
            if (date.toDateString() === today.toDateString()) {
                dayCell.classList.add("today");
            }

            dayCell.onclick = () => {
                selectedDate = date;
                document.querySelectorAll(".calendar-day").forEach(cell => cell.classList.remove("selected"));
                dayCell.classList.add("selected");
                updateReservationDate();
            };

            daysContainer.appendChild(dayCell);
        }

        calendarContainer.appendChild(daysContainer);
    }

    function updateReservationDate() {
        if (selectedDate && timeSelection.value) {
            const selectedTime = timeSelection.value;
            const [hours, minutes] = selectedTime.split(":");
            selectedDate.setHours(hours, minutes);

            reservationDateInput.value = selectedDate.toISOString();
            console.log("Selected reservation date:", reservationDateInput.value);
        }
    }

    timeSelection.addEventListener("change", updateReservationDate);

    createCalendar(today.getFullYear(), today.getMonth());

    form.addEventListener("submit", (e) => {
        if (!reservationDateInput.value) {
            e.preventDefault();
            alert("Пожалуйста, выберите дату и время для бронирования!");
        }
    });
});