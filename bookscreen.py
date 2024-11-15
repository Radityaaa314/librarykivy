from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.lang import Builder
from pengembalian import PengembalianScreen  # Mengimpor PengembalianScreen dari pengembalian.py
from riwayat import RiwayatScreen  # Mengimpor RiwayatScreen dari riwayat.py
from profil import ProfilScreen  # Mengimpor ProfilScreen dari profil.py

# Load the .kv file for BookScreen
Builder.load_file('bookscreen.kv')

class BookScreen(Screen):
    def __init__(self, **kwargs):
        super(BookScreen, self).__init__(**kwargs)

    def on_enter(self):
        # Fungsi yang dijalankan ketika layar ini ditampilkan
        pass

    def logout(self, instance):
        # Navigasi ke layar login
        self.manager.current = 'login_screen'

    def navigate_to_riwayat(self):
        # Navigasi ke layar riwayat
        self.manager.current = 'riwayat_screen'

    def navigate_to_profil(self):
        # Navigasi ke layar profil
        self.manager.current = 'profil_screen'
