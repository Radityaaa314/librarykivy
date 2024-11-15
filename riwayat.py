from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.lang import Builder
from datetime import datetime
import pyrebase
from config import get_firebase_config

config = get_firebase_config()
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# Load the kv file
Builder.load_file('riwayat.kv')

class RiwayatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.riwayat_pinjam = []  # List to store borrowing history
        self.riwayat_kembali = []  # List to store return history

    def on_enter(self):
        # Load both borrowing and return history when the screen is opened
        self.load_riwayat_pinjam()
        self.load_riwayat_kembali()

    def load_riwayat_pinjam(self):
        user_id = "user"  # Replace with actual user ID

        try:
            # Retrieve borrowing history from Firebase
            riwayat_data = db.child("book_loans").child(user_id).get()

            # Clear the current list and widgets
            self.riwayat_pinjam.clear()
            self.ids.book_list.clear_widgets()

            if riwayat_data.each():
                for record in riwayat_data.each():
                    book_title = record.val().get("book_title", "Unknown Title")
                    borrow_date = record.val().get("borrow_date", "Unknown Date")
                    self.add_riwayat_pinjam(book_title, borrow_date)
            else:
                self.show_popup("Info", "Tidak ada riwayat peminjaman.")
        except Exception as e:
            self.show_popup("Error", f"Gagal memuat riwayat peminjaman: {e}")

    def load_riwayat_kembali(self):
        user_id = "user"  # Replace with actual user ID

        try:
            # Retrieve return history from Firebase
            pengembalian_data = db.child("book_returns").child(user_id).get()

            # Clear the current list and widgets
            self.riwayat_kembali.clear()

            if pengembalian_data.each():
                for record in pengembalian_data.each():
                    book_title = record.val().get("book_title", "Unknown Title")
                    return_date = record.val().get("return_date", "Unknown Date")
                    fine = record.val().get("fine", 0)
                    self.add_riwayat_kembali(book_title, return_date, fine)
            else:
                self.show_popup("Info", "Tidak ada riwayat pengembalian.")
        except Exception as e:
            self.show_popup("Error", f"Gagal memuat riwayat pengembalian: {e}")

    def add_riwayat_pinjam(self, book_title, borrow_date):
        # Format and add the borrowing record to the screen
        riwayat = f"{book_title} - Dipinjam pada {borrow_date}"
        if riwayat not in self.riwayat_pinjam:
            self.riwayat_pinjam.append(riwayat)
            self.update_riwayat()
        else:
            self.show_popup("Error", "Riwayat peminjaman sudah ada.")

    def add_riwayat_kembali(self, book_title, return_date, fine):
        # Format and add the return record to the screen
        riwayat = f"{book_title} - Dikembalikan pada {return_date} (Denda: {fine} Rupiah)"
        if riwayat not in self.riwayat_kembali:
            self.riwayat_kembali.append(riwayat)
            self.update_riwayat()
        else:
            self.show_popup("Error", "Riwayat pengembalian sudah ada.")

    def update_riwayat(self):
        # Clear old widgets and add each borrowing and return record to the list
        self.ids.book_list.clear_widgets()

        # Display borrowing history
        self.ids.book_list.add_widget(Label(text="Riwayat Peminjaman", bold=True, size_hint_y=None, height=dp(30)))
        for riwayat in self.riwayat_pinjam:
            book_label = Label(text=riwayat, size_hint_y=None, height=dp(30))
            self.ids.book_list.add_widget(book_label)

        # Display return history
        self.ids.book_list.add_widget(Label(text="Riwayat Pengembalian", bold=True, size_hint_y=None, height=dp(30)))
        for riwayat in self.riwayat_kembali:
            book_label = Label(text=riwayat, size_hint_y=None, height=dp(30))
            self.ids.book_list.add_widget(book_label)

    def go_back(self):
        # Navigate back to BookScreen
        self.manager.current = 'book_screen'

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=dp(10))
        popup_label = Label(text=message)
        close_btn = Button(text="Close", size_hint_y=None, height=dp(40))

        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_btn)

        popup = Popup(title=title, content=popup_layout, size_hint=(None, None), size=(dp(300), dp(200)))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()
