from tkinter import *
import requests
import tkintermapview
from bs4 import BeautifulSoup
from tkinter import messagebox

def sprawdz_haslo():
    root = Tk()
    root.title("Uwierzytelnianie")

    def sprawdz():
        wprowadzone_haslo = entry.get()
        poprawne_haslo = "1"

        if wprowadzone_haslo == poprawne_haslo:
            messagebox.showinfo("Uwierzytelniono (:D)", "Haslo poprawne. Mozesz kontynuowac --->.")
            root.destroy()
            uruchom_program()
        else:
            messagebox.showerror("Blad uwierzytelniania :(", "Haslo niepoprawne :o.")

    Label(root, text="Podaj haslo:").pack()
    entry = Entry(root, show="*")
    entry.pack()

    Button(root, text="Sprawdź", command=sprawdz).pack()

    root.mainloop()

def uruchom_program():
    biura = []

    class Biuro:
        def __init__(self, nazwa, lokalizacja, lokalizacja_hotel):
            self.nazwa = nazwa
            self.lokalizacja = lokalizacja
            self.lokalizacja_hotel = lokalizacja_hotel
            self.pracownicy = []
            self.wspolrzedne = self.pobierz_wspolrzedne(self.lokalizacja)
            self.marker_biuro = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"{self.nazwa}")
            self.marker_hotel = map_widget.set_marker(*self.pobierz_wspolrzedne(self.lokalizacja_hotel), text=f"Hotel {self.nazwa}")

        def pobierz_wspolrzedne(self, lokalizacja):
            url = f'https://pl.wikipedia.org/wiki/{lokalizacja}'
            response = requests.get(url)
            response_html = BeautifulSoup(response.text, 'html.parser')
            lat = float(response_html.select('.latitude')[1].text.replace(",", "."))
            lon = float(response_html.select('.longitude')[1].text.replace(",", "."))
            return lat, lon

        def dodaj_pracownika(self, pracownik):
            self.pracownicy.append(pracownik)
            pracownik.wspolrzedne = self.wspolrzedne
            pracownik.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"{pracownik.imie}")

        def usun_pracownika(self, pracownik):
            pracownik.marker.delete()
            self.pracownicy.remove(pracownik)

        def usun(self):
            self.marker_biuro.delete()
            self.marker_hotel.delete()
            for pracownik in self.pracownicy:
                pracownik.marker.delete()

    class Pracownik:
        def __init__(self, imie, staz):
            self.imie = imie
            self.staz = staz
            self.wspolrzedne = None
            self.marker = None

    def lista_biur():
        listbox_lista_biur.delete(0, END)
        for biuro in biura:
            listbox_lista_biur.insert(END, biuro.nazwa)

    def lista_pracownikow():
        listbox_lista_pracownikow.delete(0, END)
        if listbox_lista_biur.curselection():
            biuro = biura[listbox_lista_biur.curselection()[0]]
            for pracownik in biuro.pracownicy:
                listbox_lista_pracownikow.insert(END, f"{pracownik.imie} - {pracownik.staz} lat")

    def dodaj_biuro():
        nazwa = entry_nazwa_biuro.get()
        lokalizacja = entry_lokalizacja_biuro.get()
        lokalizacja_hotel = entry_lokalizacja_hotel.get()
        biuro = Biuro(nazwa, lokalizacja, lokalizacja_hotel)
        biura.append(biuro)
        lista_biur()
        entry_nazwa_biuro.delete(0, END)
        entry_lokalizacja_biuro.delete(0, END)
        entry_lokalizacja_hotel.delete(0, END)
        entry_nazwa_biuro.focus()

    def dodaj_pracownika():
        imie = entry_imie_pracownik.get()
        staz = entry_staz_pracownik.get()
        if listbox_lista_biur.curselection():
            biuro = biura[listbox_lista_biur.curselection()[0]]
            pracownik = Pracownik(imie, staz)
            biuro.dodaj_pracownika(pracownik)
            lista_pracownikow()
            entry_imie_pracownik.delete(0, END)
            entry_staz_pracownik.delete(0, END)
            entry_imie_pracownik.focus()
        else:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać biuro przed dodaniem pracownika.")

    def usun_biuro():
        if listbox_lista_biur.curselection():
            index = listbox_lista_biur.curselection()[0]
            biura[index].usun()
            del biura[index]
            lista_biur()
            listbox_lista_pracownikow.delete(0, END)
        else:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać biuro przed usunięciem.")

    def edytuj_biuro():
        if listbox_lista_biur.curselection():
            map_widget.delete_all_marker()
            index = listbox_lista_biur.curselection()[0]
            entry_nazwa_biuro.insert(0, biura[index].nazwa)
            entry_lokalizacja_biuro.insert(0, biura[index].lokalizacja)
            entry_lokalizacja_hotel.insert(0, biura[index].lokalizacja_hotel)
            button_dodaj_biuro.config(text="Zapisz zmiany", command=lambda: aktualizuj_biuro(index))
        else:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać biuro przed edytowaniem.")

    def aktualizuj_biuro(index):
        biura[index].marker_biuro.delete()
        biura[index].marker_hotel.delete()
        biura[index].nazwa = entry_nazwa_biuro.get()
        biura[index].lokalizacja = entry_lokalizacja_biuro.get()
        biura[index].lokalizacja_hotel = entry_lokalizacja_hotel.get()
        biura[index].wspolrzedne = biura[index].pobierz_wspolrzedne(biura[index].lokalizacja)
        biura[index].marker_biuro = map_widget.set_marker(biura[index].wspolrzedne[0], biura[index].wspolrzedne[1], text=f"{biura[index].nazwa}")
        biura[index].marker_hotel = map_widget.set_marker(*biura[index].pobierz_wspolrzedne(biura[index].lokalizacja_hotel), text=f"Hotel {biura[index].nazwa}")
        lista_biur()
        button_dodaj_biuro.config(text="Dodaj Biuro", command=dodaj_biuro)
        entry_nazwa_biuro.delete(0, END)
        entry_lokalizacja_biuro.delete(0, END)
        entry_lokalizacja_hotel.delete(0, END)
        entry_nazwa_biuro.focus()

    def pokaz_biuro():
        if listbox_lista_biur.curselection():
            index = listbox_lista_biur.curselection()[0]
            biuro = biura[index]
            map_widget.set_position(biuro.wspolrzedne[0], biuro.wspolrzedne[1])
            map_widget.set_zoom(12)
            lista_pracownikow()


    def pokaz_wszystkie_biura():
        map_widget.delete_all_marker()
        for biuro in biura:
            map_widget.set_marker(biuro.wspolrzedne[0], biuro.wspolrzedne[1], text=f"{biuro.nazwa}")
            map_widget.set_marker(*biuro.pobierz_wspolrzedne(biuro.lokalizacja_hotel), text=f"Hotel {biuro.nazwa}")
        map_widget.set_zoom(6)

    def pokaz_wszystkich_pracownikow():
        map_widget.delete_all_marker()
        for biuro in biura:
            for pracownik in biuro.pracownicy:
                map_widget.set_marker(pracownik.wspolrzedne[0], pracownik.wspolrzedne[1], text=f"{pracownik.imie}")
        map_widget.set_zoom(6)

    def pokaz_pracownikow_biura():
        map_widget.delete_all_marker()
        if listbox_lista_biur.curselection():
            index = listbox_lista_biur.curselection()[0]
            biuro = biura[index]
            for pracownik in biuro.pracownicy:
                map_widget.set_marker(pracownik.wspolrzedne[0], pracownik.wspolrzedne[1], text=f"{pracownik.imie}")
            map_widget.set_zoom(12)
        else:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać biuro przed pokazaniem pracowników.")

    def pokaz_hotele_wspolpracujace():
        if listbox_lista_biur.curselection():
            map_widget.delete_all_marker()
            index = listbox_lista_biur.curselection()[0]
            biuro = biura[index]
            map_widget.set_marker(*biuro.wspolrzedne, text=f"Biuro {biuro.nazwa}")
            map_widget.set_marker(*biuro.pobierz_wspolrzedne(biuro.lokalizacja_hotel), text=f"Hotel {biuro.nazwa}")
            map_widget.set_zoom(6)
        else:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać biuro przed pokazaniem hoteli współpracujących.")

    def usun_pracownika():
        if listbox_lista_pracownikow.curselection():
            if listbox_lista_biur.curselection():
                index_biuro = listbox_lista_biur.curselection()[0]
                index_pracownik = listbox_lista_pracownikow.curselection()[0]
                pracownik = biura[index_biuro].pracownicy[index_pracownik]
                biura[index_biuro].usun_pracownika(pracownik)
                lista_pracownikow()
            else:
                if len(biura) > 0:
                    index_biuro = 0
                    index_pracownik = listbox_lista_pracownikow.curselection()[0]
                    pracownik = biura[index_biuro].pracownicy[index_pracownik]
                    biura[index_biuro].usun_pracownika(pracownik)
                    lista_pracownikow()
        else:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać pracownika przed usunięciem.")

    def pokaz_wszystkich_pracownikow1():
        listbox_lista_pracownikow.delete(0, END)
        for biuro in biura:
            for pracownik in biuro.pracownicy:
                listbox_lista_pracownikow.insert(END, f"{pracownik.imie} - {pracownik.staz} lat")

    def edytuj_pracownika():
        if listbox_lista_pracownikow.curselection():
            index_pracownik = listbox_lista_pracownikow.curselection()[0]
            if listbox_lista_biur.curselection():
                index_biuro = listbox_lista_biur.curselection()[0]
            else:
                index_biuro = 0
            pracownik = biura[index_biuro].pracownicy[index_pracownik]
            entry_imie_pracownik.insert(0, pracownik.imie)
            entry_staz_pracownik.insert(0, pracownik.staz)
            button_dodaj_pracownika.config(text="Zapisz zmiany",
                                           command=lambda: aktualizuj_pracownika(index_biuro, index_pracownik))
        else:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać pracownika przed edytowaniem.")

    def aktualizuj_pracownika(index_biuro, index_pracownik):
        pracownik = biura[index_biuro].pracownicy[index_pracownik]
        pracownik.imie = entry_imie_pracownik.get()
        pracownik.staz = entry_staz_pracownik.get()
        pracownik.marker.delete()
        pracownik.marker = map_widget.set_marker(pracownik.wspolrzedne[0], pracownik.wspolrzedne[1],
                                                 text=f"{pracownik.imie}")
        lista_pracownikow()
        button_dodaj_pracownika.config(text="Dodaj Pracownika", command=dodaj_pracownika)
        button_edytuj_pracownika.config(state='normal')
        entry_imie_pracownik.delete(0, END)
        entry_staz_pracownik.delete(0, END)
        entry_imie_pracownik.focus()

    root = Tk()
    root.title("Mapa biur")

    frame = Frame(root)
    frame.pack(side=LEFT, padx=10)

    label_lista_biur = Label(frame, text="Lista biur: ")
    label_lista_biur.pack()

    listbox_lista_biur = Listbox(frame, width=50)
    listbox_lista_biur.pack()
    listbox_lista_biur.bind('<<ListboxSelect>>', lambda event: pokaz_biuro())

    label_lista_pracownikow = Label(frame, text="Lista Pracowników: ")
    label_lista_pracownikow.pack()

    listbox_lista_pracownikow = Listbox(frame, width=50)
    listbox_lista_pracownikow.pack()

    button_usun_biuro = Button(frame, text="Usuń Biuro", command=usun_biuro)
    button_usun_biuro.pack(pady=10)

    button_edytuj_biuro = Button(frame, text="Edytuj Biuro", command=edytuj_biuro)
    button_edytuj_biuro.pack(pady=10)

    button_pokaz_wszystkie_biura = Button(frame, text="Pokaż Wszystkie Biura i Hotele", command=pokaz_wszystkie_biura)
    button_pokaz_wszystkie_biura.pack(pady=10)

    button_pokaz_wszystkich_pracownikow = Button(frame, text="Pokaż Wszystkich Pracowników", command=pokaz_wszystkich_pracownikow)
    button_pokaz_wszystkich_pracownikow.pack(pady=10)

    button_pokaz_prac_bi = Button(frame, text="Pokaż pracowników biura", command=pokaz_pracownikow_biura)
    button_pokaz_prac_bi.pack(pady=10)

    button_pokaz_wszystkich_pracownikow1 = Button(frame, text="Pokaż Wszystkich Pracowników na liście", command=pokaz_wszystkich_pracownikow1)
    button_pokaz_wszystkich_pracownikow1.pack(pady=10)

    button_pokaz_hotele = Button(frame, text="Pokaż Hotele Współpracujące", command=pokaz_hotele_wspolpracujace)
    button_pokaz_hotele.pack(pady=10)

    frame_dodaj_biuro = Frame(root)
    frame_dodaj_biuro.pack(side=LEFT, padx=10)

    label_nazwa_biuro = Label(frame_dodaj_biuro, text="Nazwa Biura:")
    label_nazwa_biuro.pack()
    entry_nazwa_biuro = Entry(frame_dodaj_biuro)
    entry_nazwa_biuro.pack()

    label_lokalizacja_biuro = Label(frame_dodaj_biuro, text="Lokalizacja Biura:")
    label_lokalizacja_biuro.pack()
    entry_lokalizacja_biuro = Entry(frame_dodaj_biuro)
    entry_lokalizacja_biuro.pack()

    label_lokalizacja_hotel = Label(frame_dodaj_biuro, text="Lokalizacja Hotelu:")
    label_lokalizacja_hotel.pack()
    entry_lokalizacja_hotel = Entry(frame_dodaj_biuro)
    entry_lokalizacja_hotel.pack()

    button_dodaj_biuro = Button(frame_dodaj_biuro, text="Dodaj Biuro", command=dodaj_biuro)
    button_dodaj_biuro.pack(pady=10)

    frame_dodaj_pracownika = Frame(root)
    frame_dodaj_pracownika.pack(side=LEFT, padx=10)

    label_imie_pracownik = Label(frame_dodaj_pracownika, text="Imię pracownika:")
    label_imie_pracownik.pack()
    entry_imie_pracownik = Entry(frame_dodaj_pracownika)
    entry_imie_pracownik.pack()

    label_staz_pracownik = Label(frame_dodaj_pracownika, text="Staż pracownika:")
    label_staz_pracownik.pack()
    entry_staz_pracownik = Entry(frame_dodaj_pracownika)
    entry_staz_pracownik.pack()

    button_dodaj_pracownika = Button(frame_dodaj_pracownika, text="Dodaj pracownika", command=dodaj_pracownika)
    button_dodaj_pracownika.pack(pady=10)

    button_usun_pracownika = Button(frame_dodaj_pracownika, text="Usuń pracownika", command=usun_pracownika)
    button_usun_pracownika.pack(pady=10)

    button_edytuj_pracownika = Button(frame_dodaj_pracownika, text="Edytuj pracownika", command=edytuj_pracownika)
    button_edytuj_pracownika.pack(pady=10)

    frame_mapa = Frame(root)
    frame_mapa.pack(side=LEFT, padx=10)

    map_widget = tkintermapview.TkinterMapView(frame_mapa, width=800, height=600, corner_radius=0)
    map_widget.pack()
    map_widget.set_position(52.2297, 21.0122)
    map_widget.set_zoom(6)

    root.mainloop()

if __name__ == "__main__":
    sprawdz_haslo()
