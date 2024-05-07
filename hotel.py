from abc import ABC, abstractmethod
from datetime import datetime
import tkinter as tk
from tkcalendar import Calendar

class Room(ABC):
    def __init__(self, room_number: int, price: int):
        self.room_number = room_number
        self.price = price
        self.bookings = []

    def is_available(self, start_date: datetime, end_date: datetime) -> bool:
        for booking in self.bookings:
            if not (booking['end_date'] < start_date or booking['start_date'] > end_date):
                return False
        return True

    def cancel_booking(self, start_date: datetime) -> None:
        self.bookings = [booking for booking in self.bookings if booking['start_date']!= start_date]

    def book(self, start_date: datetime, end_date: datetime) -> str:
        if self.is_available(start_date, end_date):
            self.bookings.append({'start_date': start_date, 'end_date': end_date})
            return f"Room {self.room_number} booked from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}."
        else:
            return f"Room {self.room_number} is already booked for this period."

    def get_bookings(self) -> str:
        booking_date_ranges = []
        for booking in self.bookings:
            start_date_str = booking['start_date'].strftime('%Y-%m-%d')
            end_date_str = booking['end_date'].strftime('%Y-%m-%d')
            booking_date_ranges.append(f"{start_date_str} - {end_date_str}")
        return ", ".join(booking_date_ranges)

    @abstractmethod
    def __str__(self) -> str:
        pass

class SingleRoom(Room):
    def __str__(self) -> str:
        bookings_str = self.get_bookings()
        return f"Single room. Room number: {self.room_number}, Price: {self.price}, Bookings: {bookings_str if bookings_str else 'No bookings'}"

class DoubleRoom(Room):
    def __str__(self) -> str:
        bookings_str = self.get_bookings()
        return f"Double room. Room number: {self.room_number}, Price: {self.price}, Bookings: {bookings_str if bookings_str else 'No bookings'}"

class Hotel:
    def __init__(self):
        self.rooms = []

    def add_room(self, room: Room) -> None:
        self.rooms.append(room)

    def load_data(self) -> None:
        self.add_room(SingleRoom(101, 50000))
        self.add_room(DoubleRoom(102, 60000))

    def get_room_bookings(self) -> str:
        return '\n'.join(str(room) for room in self.rooms)

    def book_room(self, room_number: int, start_date: datetime, end_date: datetime) -> str:
        for room in self.rooms:
            if room.room_number == room_number:
                return room.book(start_date, end_date)
        return "Room not found."

def create_gui(hotel: Hotel) -> None:
    root = tk.Tk()
    root.title("Hotel Booking System")

    def show_bookings():
        bookings_text.delete(1.0, tk.END)
        bookings_text.insert(tk.END, hotel.get_room_bookings())

    def book_room():
        try:
            room_number = int(room_number_entry.get())
            start_date = calendar.get_date()
            end_date = calendar.get_date()
            result = hotel.book_room(room_number, start_date, end_date)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, result)
        except ValueError:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Invalid date format. Please use yyyy-mm-dd.")

    room_number_label = tk.Label(root, text="Room number:")
    room_number_label.pack()
    room_number_entry = tk.Entry(root)
    room_number_entry.pack()

    calendar = Calendar(root, selectmode='day')
    calendar.pack(pady=20)

    start_date_label = tk.Label(root, text="Start date:")
    start_date_label.pack()
    start_date_entry = tk.Entry(root)
    start_date_entry.pack()

    end_date_label = tk.Label(root, text="End date:")
    end_date_label.pack()
    end_date_entry = tk.Entry(root)
    end_date_entry.pack()

    book_button = tk.Button(root, text="Book", command=book_room)
    book_button.pack()

    result_text = tk.Text(root, height=10, width=50)
    result_text.pack()

    bookings_button = tk.Button(root, text="Show bookings", command=show_bookings)
    bookings_button.pack()

    bookings_text = tk.Text(root, height=20, width=50)
    bookings_text.pack()

    root.mainloop()

if __name__ == "__main__":
    hotel = Hotel()
    hotel.load_data()
    create_gui(hotel)