from abc import ABC, abstractmethod
from datetime import datetime
import tkinter as tk
import tkcalendar as tkcalendar

class szoba(ABC):
    def __init__(self, szoba_szam: int, ar: int):
        self.szoba_szam = szoba_szam
        self.ar = ar
        self.foglalas = []

    def is_available(self, erkezes: datetime, tavozas: datetime) -> bool:
        for booking in self.foglalas:
            if not (booking['tavozas'] < erkezes or booking['erkezes'] > tavozas):
                return False
        return True

    def cancel_booking(self, erkezes: datetime) -> None:
        self.foglalas = [booking for booking in self.foglalas if booking['erkezes']!= erkezes]

    def book(self, erkezes: datetime, tavozas: datetime) -> str:
        if self.is_available(erkezes, tavozas):
            self.foglalas.append({'erkezes': erkezes, 'tavozas': tavozas})
            return f"A szoba {self.szoba_szam} {erkezes.strftime('%Y-%m-%d')}-tól {tavozas.strftime('%Y-%m-%d')}-ig lefoglalva."
        else:
            return f"{self.szoba_szam} "

    def get_foglalas(self) -> str:
        booking_date_ranges = []
        for booking in self.foglalas:
            erkezes_str = booking['erkezes'].strftime('%Y-%m-%d')
            tavozas_str = booking['tavozas'].strftime('%Y-%m-%d')
            booking_date_ranges.append(f"{erkezes_str} - {tavozas_str}")
        return ", ".join(booking_date_ranges)

    @abstractmethod
    def __str__(self) -> str:
        pass

class Egyagyasszoba(szoba):
    def __str__(self) -> str:
        foglalas_str = self.get_foglalas()
        return f"Ez itt Egyágyas szoba, Száma: {self.szoba_szam}, ára: {self.ar}Ft, állása: {foglalas_str if foglalas_str else 'üres szoba'}"

class Ketagyasszoba(szoba):
    def __str__(self) -> str:
        foglalas_str = self.get_foglalas()
        return f"Ez itt egy Kétágyas szoba, Száma: {self.szoba_szam}, ar: {self.ar}Ft, állása {foglalas_str if foglalas_str else 'üres szoba'}"

class Hotel:
    def __init__(self):
        self.szobas = []

    def add_szoba(self, szoba: szoba) -> None:
        self.szobas.append(szoba)

    def load_data(self) -> None:
        self.add_szoba(Egyagyasszoba(101, 50000))
        self.add_szoba(Ketagyasszoba(102, 60000))

    def get_szoba_foglalas(self) -> str:
        return '\n'.join(str(szoba) for szoba in self.szobas)


    def book_szoba(self, szoba_szam: int, erkezes: datetime, tavozas: datetime) -> str:
        for szoba in self.szobas:
            if szoba.szoba_szam == szoba_szam:
                return szoba.book(erkezes, tavozas)
        return "A szoba nem létezik. :("

def create_gui(hotel: Hotel) -> None:
    root = tk.Tk()
    root.title("GDE_OOP_HOTEL")

    def show_foglalas():
        foglalas_text.delete(1.0, tk.END)
        foglalas_text.insert(tk.END, hotel.get_szoba_foglalas())

    def book_szoba():
    try:
        szoba_szam_entry = tk.Entry(root)  # Create a Tkinter Entry widget for the user to input the room number
        szoba_szam_entry.pack()
        

        erkezes = erkezes_entry.get_date()
        tavozas = tavozas_entry.get_date()

        # Get the room number from the Entry widget
        szoba_szam = int(szoba_szam_entry.get())

        result = hotel.book_szoba(szoba_szam, erkezes, tavozas)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result)
    except ValueError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Hiányzik a szobaszám!")
    except Exception as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Valami hiba történt: {e}")

    szoba_listbox = tk.Listbox(root)
    for szoba in hotel.szobas:
        szoba_listbox.insert(tk.END, f"{szoba.szoba_szam}: {szoba.__class__.__name__}")
    szoba_listbox.pack()

    erkezes_label = tk.Label(root, text="Érkezés:")
    erkezes_label.pack()
    erkezes_entry = tkcalendar.DateEntry(root, mindate=None)
    erkezes_entry.pack()

    tavozas_label = tk.Label(root, text="Távozás:")
    tavozas_label.pack()
    tavozas_entry = tkcalendar.DateEntry(root, mindate=None)
    tavozas_entry.pack()

    book_button = tk.Button(root, text="Book", command=book_szoba)
    book_button.pack()

    result_text = tk.Text(root, height=10, width=75)
    result_text.pack()

    foglalas_button = tk.Button(root, text="Az eddigi foglalások megjelenítése", command=show_foglalas)
    foglalas_button.pack()

    foglalas_text = tk.Text(root, height=10, width=75)
    foglalas_text.pack()

    root.mainloop()

if __name__ == "__main__":
    hotel = Hotel()
    hotel.load_data()
    create_gui(hotel)