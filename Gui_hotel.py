from abc import ABC, abstractmethod
from datetime import datetime
import tkinter as tk
import tkcalendar as tkcalendar
from datetime import timedelta

class szoba(ABC):
    def __init__(self, szoba_szam: int, ar: int):
        self.szoba_szam = szoba_szam
        self.ar = ar
        self.foglalas = []

    def is_available(self, erkezes: datetime, tavozas: datetime) -> bool:
        for foglalas in self.foglalas:
            if not (foglalas['tavozas'] < erkezes or foglalas['erkezes'] > tavozas):
                return False
        return True

    def cancel_foglalas(self, erkezes: datetime) -> None:
        self.foglalas = [foglalas for foglalas in self.foglalas if foglalas['erkezes']!= erkezes]

    def book(self, erkezes: datetime, tavozas: datetime) -> str:
        if self.is_available(erkezes, tavozas):
            self.foglalas.append({'erkezes': erkezes, 'tavozas': tavozas})
            return f"A szoba {self.szoba_szam} {erkezes.strftime('%Y-%m-%d')}-tól {tavozas.strftime('%Y-%m-%d')}-ig lefoglalva."
        else:
            return f"{self.szoba_szam} "

    def get_foglalas(self) -> str:
        foglalas_date_ranges = []
        for foglalas in self.foglalas:
            erkezes_str = foglalas['erkezes'].strftime('%Y-%m-%d')
            tavozas_str = foglalas['tavozas'].strftime('%Y-%m-%d')
            foglalas_date_ranges.append(f"{erkezes_str} - {tavozas_str}")
        return ", ".join(foglalas_date_ranges)

    @abstractmethod
    def __str__(self) -> str:
        pass

class Egyagyasszoba(szoba):
    def __str__(self) -> str:
        foglalas_str = self.get_foglalas()
        return f"Ez itt Egyágyas szoba, Száma: {self.szoba_szam}, ára: {self.ar}Ft, jelenleg {'foglalt.' if foglalas_str else 'üres.'}"

class Ketagyasszoba(szoba):
    def __str__(self) -> str:
        foglalas_str = self.get_foglalas()
        return f"Ez itt egy Kétágyas szoba, Száma: {self.szoba_szam}, ára: {self.ar}Ft, jelenleg {'foglalt.' if foglalas_str else 'üres.'}"

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
    root.geometry("800x600")  

    szoba_label = tk.Label(root, text="Válasszon szobát:")
    szoba_label.pack()

    szoba_var = tk.StringVar()
    szoba_var.set(next((f"{szoba.szoba_szam}: {szoba.__class__.__name__}" for szoba in hotel.szobas), None))  

    szoba_option = tk.OptionMenu(root, szoba_var, *[f"{szoba.szoba_szam}: {szoba.__class__.__name__}" for szoba in hotel.szobas])
    szoba_option.pack()

    erkezes_label = tk.Label(root, text="Érkezés:")
    erkezes_label.pack()
    erkezes_entry = tkcalendar.DateEntry(root, mindate=None)
    erkezes_entry.pack()

    tavozas_label = tk.Label(root, text="Távozás:")
    tavozas_label.pack()
    tavozas_entry = tkcalendar.DateEntry(root, mindate=None)

    def update_tavozas_mindate(event):
        erkezes_date = erkezes_entry.get_date()
        if erkezes_date:
            tavozas_entry.config(mindate=erkezes_date + timedelta(days=2))

    erkezes_entry.bind("<<DateEntrySelected>>", update_tavozas_mindate)
    tavozas_entry.pack()

    def calculate_ar():
        try:
            erkezes = erkezes_entry.get_date()
            tavozas = tavozas_entry.get_date()

            if erkezes >= tavozas:
                ar_text.delete(1.0, tk.END)
                ar_text.insert(tk.END, "A távozás dátuma nem lehet korábbi, mint az érkezés dátuma!")
                return

            
            szoba_szam, szoba_type = szoba_var.get().split(":")
            szoba_szam = int(szoba_szam)
            for szoba in hotel.szobas:
                if szoba.szoba_szam == szoba_szam:
                    ar = szoba.ar
                    break

          
            napok_szama = (tavozas - erkezes).days
            total_ar = napok_szama * ar

            
            ar_text.delete(1.0, tk.END)
            ar_text.insert(tk.END, f"A foglalás ára: {total_ar} Ft.")
        except ValueError:
            ar_text.delete(1.0, tk.END)
            ar_text.insert(tk.END, "Hiányzik a szobaszám vagy a dátum!")
        except Exception as e:
            ar_text.delete(1.0, tk.END)
            ar_text.insert(tk.END, f"Valami hiba történt: {e}")

    def book_room():
        try:
            erkezes = erkezes_entry.get_date()
            tavozas = tavozas_entry.get_date()
            
            if erkezes > tavozas:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "A távozás dátuma nem lehet korábbi, mint az érkezés dátuma!")
                return

            
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

    ar_button = tk.Button(root, text="Számítás", command=calculate_ar)
    ar_button.pack()

    ar_text = tk.Text(root, height=1, width=60)
    ar_text.pack()

    book_button = tk.Button(root, text="Foglalás!", command=book_room)
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