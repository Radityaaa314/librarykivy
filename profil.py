from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.lang import Builder

# Load the .kv file
Builder.load_file('profil.kv')

class ProfilPenggunaForm(BoxLayout):
    def __init__(self, **kwargs):
        super(ProfilPenggunaForm, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(10)

        # Background styling for Profile with Rectangle
        with self.canvas.before:
            Color(0.96, 0.94, 0.91, 1)  # Cream background for the profile section
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Updated profile data
        profile_data = {
            "name": "Radit",
            "email": "radit29@gmail.com",
            "join_date": "01-01-2020",  # Example join date
        }

        # Display the profile information
        self.add_widget(Label(text=f"Nama: {profile_data['name']}", font_size='18sp', color=(0, 0, 0, 1), size_hint_y=None, height=dp(30)))
        self.add_widget(Label(text=f"Email: {profile_data['email']}", font_size='18sp', color=(0, 0, 0, 1), size_hint_y=None, height=dp(30)))
        self.add_widget(Label(text=f"Tanggal Bergabung: {profile_data['join_date']}", font_size='18sp', color=(0, 0, 0, 1), size_hint_y=None, height=dp(30)))

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class BorrowingHistory(BoxLayout):
    def __init__(self, **kwargs):
        super(BorrowingHistory, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)

        # Background styling for Borrowing History with Rectangle
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Light gray background for the history section
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Add placeholder history data (Replace with actual data dynamically)
        self.add_widget(Label(text="Riwayat Peminjaman Buku:", font_size='18sp', color=(0, 0, 0, 1)))

        # Placeholder for books the user has borrowed
        self.add_widget(Label(text="Buku 1: The Great Gatsby", font_size='16sp', color=(0, 0, 0, 1)))
        self.add_widget(Label(text="Buku 2: To Kill A Mockingbird", font_size='16sp', color=(0, 0, 0, 1)))
        self.add_widget(Label(text="Buku 3: Little Women", font_size='16sp', color=(0, 0, 0, 1)))

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ProfilScreen(Screen):
    def __init__(self, **kwargs):
        super(ProfilScreen, self).__init__(**kwargs)

        # Layout utama
        main_layout = BoxLayout(orientation='vertical')

        # AnchorLayout for the "Back" button (Positioned at the top-left)
        back_layout = AnchorLayout(anchor_x='left', anchor_y='top', size_hint_y=None, height=dp(50))
        back_button = Button(text='Kembali', size_hint=(None, None), size=(dp(100), dp(40)), background_color=(0.23, 0.23, 0.23, 1))  # Dark brown
        back_button.bind(on_press=self.go_back)
        back_layout.add_widget(back_button)

        # Add the back button layout to the main layout
        main_layout.add_widget(back_layout)

        # Profil Pengguna Form (Top part)
        profile_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(250))
        profile_layout.add_widget(ProfilPenggunaForm())  # Add the profile form once
        main_layout.add_widget(profile_layout)

        # Scrollable section for Borrowing History (Bottom part)
        history_layout = ScrollView(size_hint=(1, None), height=dp(200))  # Scrollable area for the history
        history_layout.add_widget(BorrowingHistory())  # Add the borrowing history section
        main_layout.add_widget(history_layout)

        self.add_widget(main_layout)

    def go_back(self, instance):
        # Go back to the main screen (BookScreen)
        self.manager.current = 'book_screen'
