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
        return f"Ez itt Egyágyas szoba, Száma: {self.szoba_szam}, ára: {self.ar}Ft, jelenleg {foglalas_str if foglalas_str else 'üres szoba'}"

class Ketagyasszoba(szoba):
    def __str__(self) -> str:
        foglalas_str = self.get_foglalas()
        return f"Ez itt egy Kétágyas szoba, Száma: {self.szoba_szam}, ar: {self.ar}Ft, jelenleg {'foglalt.' if foglalas_str else 'üres.'}"

class Hotel:
    def __init__(self):
        self.szobas = []

    def add_szoba(self, szoba: szoba) -> None:
        self.szobas.append(szoba)

    def load_data(self) -> None:
        self.add_szoba(Egyagyasszoba(101, 20000))
        self.add_szoba(Ketagyasszoba(102, 30000))

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
    root.geometry("800x600")  # Set the GUI size to 800x600 pixels

    szoba_label = tk.Label(root, text="Válasszon szobát:")
    szoba_label.pack()

    szoba_var = tk.StringVar()
    szoba_var.set(next((f"{szoba.szoba_szam}: {szoba.__class__.__name__}" for szoba in hotel.szobas), None))  # default value

    szoba_option = tk.OptionMenu(root, szoba_var, *[f"{szoba.szoba_szam}: {szoba.__class__.__name__}" for szoba in hotel.szobas])
    szoba_option.pack()

    erkezes_label = tk.Label(root, text="Érkezés:")
    erkezes_label.pack()
    erkezes_entry = tkcalendar.DateEntry(root, mindate=None)
    erkezes_entry.pack()

    tavozas_label = tk.Label(root, text="Távozás:")
    tavozas_label.pack()
    tavozas_entry = tkcalendar.DateEntry(root, mindate=None)

    # Set the mindate of tavozas_entry to be one day after the erkezes_entry
    def update_tavozas_mindate(event):
        erkezes_date = erkezes_entry.get_date()
        if erkezes_date:
            tavozas_entry.config(mindate=erkezes_date + timedelta(days+1))

    erkezes_entry.bind("<<DateEntrySelected>>", update_tavozas_mindate)
    tavozas_entry.pack()

    def calculate_price():
        try:
            erkezes = erkezes_entry.get_date()
            tavozas = tavozas_entry.get_date()

            if erkezes >= tavozas:
                price_text.delete(1.0, tk.END)
                price_text.insert(tk.END, "A távozás dátuma nem lehet korábbi, mint az érkezés dátuma!")
                return

            # Get the room number and price from the OptionMenu
            szoba_szam, szoba_type = szoba_var.get().split(":")
            szoba_szam = int(szoba_szam)
            for szoba in hotel.szobas:
                if szoba.szoba_szam == szoba_szam:
                    price = szoba.ar
                    break

          
            napok_szama = (tavozas - erkezes).days
            total_price = napok_szama * price

            # Display the total price
            price_text.delete(1.0, tk.END)
            price_text.insert(tk.END, f"A foglalás ára: {total_price} Ft.")
        except ValueError:
            price_text.delete(1.0, tk.END)
            price_text.insert(tk.END, "Hiányzik a szobaszám vagy a dátum!")
        except Exception as e:
            price_text.delete(1.0, tk.END)
            price_text.insert(tk.END, f"Valami hiba történt: {e}")

    def book_room():
        try:
            erkezes = erkezes_entry.get_date()
            tavozas = tavozas_entry.get_date()

            if erkezes >= tavozas:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "A távozás dátuma nem lehet korábbi, mint az érkezés dátuma!")
                return

            # Get the room number from the OptionMenu
            szoba_szam = int(szoba_var.get().split(":")[0])

            result = hotel.book_szoba(szoba_szam, erkezes, tavozas)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, result)
        except ValueError:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Hiányzik a szobaszám!")
        except Exception as e:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Valami hiba történt: {e}")

    def show_foglalas():
        foglalas_text.delete(1.0, tk.END)
        foglalas_text.insert(tk.END, hotel.get_szoba_foglalas())

    price_button = tk.Button(root, text="Számítás", command=calculate_price)
    price_button.pack()

    price_text = tk.Text(root, height=1, width=60)
    price_text.pack()

    book_button = tk.Button(root, text="Book", command=book_room)
    book_button.pack()

    result_text = tk.Text(root, height=5, width=85)
    result_text.pack()

    foglalas_button = tk.Button(root, text="Az eddigi foglalások megjelenítése", command=show_foglalas)
    foglalas_button.pack()

    foglalas_text = tk.Text(root, height=5, width=85)
    foglalas_text.pack()

    root.mainloop()

if __name__ == "__main__":
    hotel = Hotel()
    hotel.load_data()
    create_gui(hotel)