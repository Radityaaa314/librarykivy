from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
import datetime
import pyrebase
from config import get_firebase_config

# Firebase initialization
config = get_firebase_config()
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Load the .kv file
Builder.load_file('pengembalian.kv')

class BookReturnForm(BoxLayout):
    def __init__(self, **kwargs):
        super(BookReturnForm, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(10)

        # Background styling with Rectangle
        with self.canvas.before:
            Color(0.96, 0.94, 0.91, 1)  # Background color: cream
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def submit(self, instance):
        nama = self.ids.nama_input.text
        judul = self.ids.judul_spinner.text
        tglkembali = self.ids.tglkembali_input.text

        if not nama or not judul or not tglkembali:
            self.show_popup("Error", "Please fill out all fields!")
            return

        try:
            # Calculate overdue days and fine
            tglWajib = [int(part) for part in tglkembali.split('-')]
            tglskg = datetime.datetime.now()
            tglDeadline = datetime.datetime(tglWajib[0], tglWajib[1], tglWajib[2])
            selisih_hari = (tglskg - tglDeadline).days
            denda = 0

            if selisih_hari > 0:
                denda = 5000 * selisih_hari

            # Save return data to Firebase
            success, message = kembalikan_buku(nama, judul, tglDeadline.strftime("%Y-%m-%d"), selisih_hari, denda)

            # Show success or error popup
            if success:
                if denda == 0:
                    self.show_popup("Success", "Buku berhasil dikembalikan tanpa denda!")
                else:
                    self.show_popup("Denda", f"Anda terlambat mengembalikan buku sebanyak {selisih_hari} hari, "
                                             f"harap membayar denda sebesar {denda} rupiah.")
            else:
                self.show_popup("Error", f"Gagal mengembalikan buku: {message}")
        except Exception as e:
            self.show_popup("Error", "Invalid date format. Please use YYYY-MM-DD.")

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=dp(10))
        popup_label = Label(text=message)
        close_btn = Button(text="Close", size_hint_y=None, height=dp(40))

        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_btn)

        popup = Popup(title=title, content=popup_layout, size_hint=(None, None), size=(dp(300), dp(200)))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class PengembalianScreen(Screen):
    def __init__(self, **kwargs):
        super(PengembalianScreen, self).__init__(**kwargs)

        # Layout utama
        main_layout = BoxLayout(orientation='vertical')

        # AnchorLayout untuk menempatkan tombol Kembali di kiri atas
        back_layout = AnchorLayout(anchor_x='left', anchor_y='top', size_hint_y=None, height=dp(50))
        back_button = Button(text='Kembali', size_hint=(None, None), size=(dp(100), dp(40)), background_color=(0.23, 0.23, 0.23, 1))  # Dark brown
        back_button.bind(on_press=self.go_back)
        back_layout.add_widget(back_button)

        # Tambahkan layout untuk tombol back
        main_layout.add_widget(back_layout)

        # Tambahkan form pengembalian
        main_layout.add_widget(BookReturnForm())

        self.add_widget(main_layout)

    def go_back(self, instance):
        # Mengganti layar ke layar utama (BookScreen)
        self.manager.current = 'book_screen'

# Fungsi untuk mencatat data pengembalian buku ke Firebase
def kembalikan_buku(nama, judul, tglDeadline, selisih_hari, denda):
    try:
        db.child("book_returns").push({
            "user_name": nama,
            "book_title": judul,
            "return_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "due_date": tglDeadline,
            "late_days": selisih_hari,
            "fine": denda
        })
        print("Pengembalian buku berhasil dicatat di Firebase")
        return True, "Pengembalian buku berhasil"
    except Exception as e:
        print(f"Gagal mencatat pengembalian buku di Firebase: {e}")
        return False, str(e)
