from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.metrics import dp
from datetime import datetime, timedelta
import pyrebase
from config import get_firebase_config

config = get_firebase_config()
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

class Book4SlideScreen(Screen):
    def __init__(self, **kwargs):
        super(Book4SlideScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='horizontal', padding=20, spacing=20)

        # Gambar buku besar di sebelah kiri atas
        self.book_image = Image(source="./assets/images/4.jpg", size_hint=(None, None), size=(dp(400), dp(600)))
        self.layout.add_widget(self.book_image)

        # Layout untuk detail buku (judul dan deskripsi) di sebelah kanan gambar
        self.details_layout = BoxLayout(orientation='vertical', spacing=10, padding=(10, 0, 0, 0))
        self.layout.add_widget(self.details_layout)

        # Judul buku
        self.title_label = Label(
            text="Pride and Prejudice",
            font_size='32sp',
            halign="left",
            valign="middle",
            size_hint_y=None,
            color=(0.2, 0.2, 0.2, 1)
        )
        self.details_layout.add_widget(self.title_label)

        # Deskripsi buku
        self.description_label = Label(
                 text="Pride and Prejudice, karya Jane Austen, mengisahkan kisah cinta antara Elizabeth Bennet dan Mr. Darcy, "
                      "dua karakter yang tampaknya sangat berbeda namun saling tertarik. Elizabeth, seorang wanita cerdas dan tegas, "
                      "mulai menganggap Mr. Darcy sombong dan angkuh karena kesan pertama yang buruk. Namun, seiring berjalannya waktu, "
                      "Elizabeth mulai menyadari bahwa penilaiannya terhadap Darcy tidak sepenuhnya tepat, dan bahwa dia memiliki kualitas "
                      "yang jauh lebih baik dari yang dia bayangkan. Novel ini mengeksplorasi tema-tema seperti kebanggaan, prasangka, "
                      "moralitas, dan perjuangan untuk mencari cinta sejati di tengah tekanan sosial dan kelas.",
            halign="left",
            valign="top",
            text_size=(dp(350), None),
            color=(0.3, 0.3, 0.3, 1)
        )
        self.details_layout.add_widget(self.description_label)

        # Tombol untuk meminjam buku
        borrow_button = Button(text="Pinjam Buku", size_hint=(None, None), size=(dp(150), dp(50)))
        borrow_button.bind(on_release=self.borrow_book)
        self.details_layout.add_widget(borrow_button)

        # Tambahkan layout utama ke layar
        self.add_widget(self.layout)

    def borrow_book(self, instance):
        user_id = "user"  # ID pengguna (harus diperoleh dari autentikasi login)
        book_id = "book4"  # ID buku yang dipinjam
        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S")  # Tanggal pengembalian (14 hari ke depan)

        # Panggil fungsi pinjam_buku untuk menyimpan data ke Firebase
        success, message = pinjam_buku(user_id, book_id, due_date)

        # Tampilkan notifikasi popup berdasarkan hasil peminjaman
        if success:
            popup_content = Label(text="Anda telah berhasil meminjam buku ini.")
        else:
            popup_content = Label(text=f"Gagal meminjam buku: {message}")

        popup = Popup(
            title="Peminjaman Buku",
            content=popup_content,
            size_hint=(None, None),
            size=(dp(300), dp(200))
        )
        popup.open()

        if success:
            self.manager.current = 'book_screen'  # Kembali ke layar utama setelah meminjam

# Fungsi untuk mencatat peminjaman buku ke Firebase
def pinjam_buku(user_id, book_id, due_date):
    try:
        # Menyimpan data peminjaman buku di Realtime Database
        db.child("book_loans").child(user_id).child(book_id).set({
            "book_id": book_id,
            "user_id": user_id,
            "borrow_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "due_date": due_date
        })
        print("Peminjaman buku berhasil")
        return True, "Peminjaman buku berhasil"
    except Exception as e:
        print(f"Peminjaman buku gagal: {e}")
        return False, str(e)
