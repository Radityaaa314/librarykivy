# database.py
import pyrebase
from config import get_firebase_config

class Database:
    config = get_firebase_config()
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    @staticmethod
    def get_all_loans():
        """Mengambil semua data peminjaman dari database."""
        try:
            loans = Database.db.child("loans").get()
            if loans.each():
                return [(loan.key(), loan.val()) for loan in loans.each()]
            return []
        except Exception as e:
            print(f"Error mengambil data peminjaman: {e}")
            return []

    @staticmethod
    def add_loan(loan_data):
        """Menambahkan data peminjaman baru ke database."""
        try:
            return Database.db.child("loans").push(loan_data)
        except Exception as e:
            print(f"Error menambahkan data peminjaman: {e}")
            raise e

    @staticmethod
    def update_loan(loan_id, loan_data):
        """Memperbarui data peminjaman yang ada di database."""
        try:
            return Database.db.child("loans").child(loan_id).update(loan_data)
        except Exception as e:
            print(f"Error memperbarui data peminjaman: {e}")
            raise e

    @staticmethod
    def delete_loan(loan_id):
        """Menghapus data peminjaman dari database."""
        try:
            return Database.db.child("loans").child(loan_id).remove()
        except Exception as e:
            print(f"Error menghapus data peminjaman: {e}")
            raise e
