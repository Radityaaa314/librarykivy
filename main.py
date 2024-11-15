from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from bookscreen import BookScreen, RiwayatScreen, ProfilScreen, PengembalianScreen
from book1slide import Book1SlideScreen
from book2slide import Book2SlideScreen
from book3slide import Book3SlideScreen
from book4slide import Book4SlideScreen
from book5slide import Book5SlideScreen
from book6slide import Book6SlideScreen
# from main import RegisterScreen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from auth import AuthService

# Memuat file KV
Builder.load_file('login.kv')
Builder.load_file('register.kv')    # Pastikan file ini ada dan sesuai

auth_service = AuthService()
class LoginScreen(Screen):
    def login(self, email, password):
        success, message = auth_service.login(email, password)
        if success:
            user_role = App.get_running_app().user_role
               # Arahkan berdasarkan peran pengguna
            if user_role == 'pengguna':
                App.get_running_app().root.current = 'book_screen'
        else:
            print(message)  # Anda dapat mengganti ini dengan popup atau notifikasi
            self.show_popup('Gagal', 'gagal login')

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()


class RegisterScreen(Screen):
    def register(self, email, password):
        success, message = auth_service.register(email, password,role='pengguna')
        if success:
            print(message)  # Feedback saat registrasi berhasil
            App.get_running_app().root.current = 'login'
        else:
            print(message)  # Anda dapat mengganti ini dengan popup atau notifikasi
            self.show_popup('Gagal', 'gagal daftar')

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        
        # Tambahkan layar login dan registrasi
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        
        # Tambahkan layar terkait buku
        sm.add_widget(BookScreen(name='book_screen'))
        sm.add_widget(RiwayatScreen(name='riwayat_screen'))
        sm.add_widget(ProfilScreen(name='profil_screen'))
        sm.add_widget(PengembalianScreen(name='pengembalian_screen'))
        
        # Tambahkan layar slide buku
        sm.add_widget(Book1SlideScreen(name='book1slide_screen'))
        sm.add_widget(Book2SlideScreen(name='book2slide_screen'))
        sm.add_widget(Book3SlideScreen(name='book3slide_screen'))
        sm.add_widget(Book4SlideScreen(name='book4slide_screen'))
        sm.add_widget(Book5SlideScreen(name='book5slide_screen'))
        sm.add_widget(Book6SlideScreen(name='book6slide_screen'))
        
        return sm

if __name__ == '__main__':
    MainApp().run()
