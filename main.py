import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookManager:
    """Класс для управления данными приложения."""
    def __init__(self, filename="data.json"):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_books(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def add_book(self, title, author, genre, pages):
        # Валидация
        if not title or not author or not genre or not pages:
            raise ValueError("Все поля должны быть заполнены.")
        try:
            pages_int = int(pages)
            if pages_int <= 0:
                raise ValueError("Количество страниц должно быть больше нуля.")
        except ValueError:
            raise ValueError("Количество страниц должно быть целым числом.")

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages_int
        }
        self.books.append(book)
        self.save_books()
        return book

    def get_all_books(self):
        return self.books

    def filter_by_genre(self, genre):
        if not genre:
            return self.books
        return [b for b in self.books if genre.lower() in b['genre'].lower()]

    def filter_by_pages(self, min_pages):
        try:
            min_pages_int = int(min_pages)
            return [b for b in self.books if b['pages'] > min_pages_int]
        except ValueError:
            raise ValueError("Для фильтрации введите целое число.")


class BookApp:
    """Класс графического интерфейса пользователя."""
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("700x500")
        
        self.manager = BookManager()

        self.create_widgets()
        self.update_treeview(self.manager.get_all_books())

    def create_widgets(self):
        # --- Фрейм ввода данных ---
        input_frame = tk.LabelFrame(self.root, text="Добавление книги", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.entry_title = tk.Entry(input_frame, width=20)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Автор:").grid(row=0, column=2, sticky="w")
        self.entry_author = tk.Entry(input_frame, width=20)
        self.entry_author.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Жанр:").grid(row=1, column=0, sticky="w")
        self.entry_genre = tk.Entry(input_frame, width=20)
        self.entry_genre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Страниц:").grid(row=1, column=2, sticky="w")
        self.entry_pages = tk.Entry(input_frame, width=20)
        self.entry_pages.grid(row=1, column=3, padx=5, pady=5)

        tk.Button(input_frame, text="Добавить книгу", command=self.add_book).grid(row=2, column=0, columnspan=4, pady=10)

        # --- Фрейм фильтрации ---
        filter_frame = tk.LabelFrame(self.root, text="Фильтры", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Жанр:").grid(row=0, column=0)
        self.filter_genre_entry = tk.Entry(filter_frame, width=15)
        self.filter_genre_entry.grid(row=0, column=1, padx=5)
        tk.Button(filter_frame, text="Найти", command=self.filter_genre).grid(row=0, column=2, padx=5)

        tk.Label(filter_frame, text="Страниц больше:").grid(row=0, column=3, padx=(20, 0))
        self.filter_pages_entry = tk.Entry(filter_frame, width=10)
        self.filter_pages_entry.grid(row=0, column=4, padx=5)
        tk.Button(filter_frame, text="Найти", command=self.filter_pages).grid(row=0, column=5, padx=5)

        tk.Button(filter_frame, text="Сбросить", command=self.reset_filters).grid(row=0, column=6, padx=10)

        # --- Таблица ---
        self.tree = ttk.Treeview(self.root, columns=("Title", "Author", "Genre", "Pages"), show='headings')
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Pages", text="Страницы")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_book(self):
        try:
            self.manager.add_book(
                self.entry_title.get().strip(),
                self.entry_author.get().strip(),
                self.entry_genre.get().strip(),
                self.entry_pages.get().strip()
            )
            # Очистка полей
            self.entry_title.delete(0, tk.END)
            self.entry_author.delete(0, tk.END)
            self.entry_genre.delete(0, tk.END)
            self.entry_pages.delete(0, tk.END)
            
            self.update_treeview(self.manager.get_all_books())
            messagebox.showinfo("Успех", "Книга успешно добавлена!")
        except ValueError as e:
            messagebox.showerror("Ошибка валидации", str(e))

    def filter_genre(self):
        genre = self.filter_genre_entry.get().strip()
        filtered = self.manager.filter_by_genre(genre)
        self.update_treeview(filtered)

    def filter_pages(self):
        pages = self.filter_pages_entry.get().strip()
        try:
            filtered = self.manager.filter_by_pages(pages)
            self.update_treeview(filtered)
        except ValueError as e:
            messagebox.showerror("Ошибка фильтрации", str(e))

    def reset_filters(self):
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_pages_entry.delete(0, tk.END)
        self.update_treeview(self.manager.get_all_books())

    def update_treeview(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for book in data:
            self.tree.insert("", tk.END, values=(book['title'], book['author'], book['genre'], book['pages']))

if __name__ == "__main__":
    root = tk.Tk()
    app = BookApp(root)
    root.mainloop()
