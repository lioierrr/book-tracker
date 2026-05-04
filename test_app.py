import unittest
import os
import json
from main import BookManager

class TestBookTracker(unittest.TestCase):
    def setUp(self):
        # Создаем временный файл для тестов
        self.test_filename = "test_data.json"
        self.manager = BookManager(self.test_filename)
        self.manager.books = [] # очистка списка
        
    def tearDown(self):
        # Удаляем тестовый файл после каждого теста
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_add_book_success(self):
        # Позитивный тест
        self.manager.add_book("1984", "Джордж Оруэлл", "Антиутопия", "328")
        self.assertEqual(len(self.manager.books), 1)
        self.assertEqual(self.manager.books[0]['title'], "1984")
        self.assertEqual(self.manager.books[0]['pages'], 328)

    def test_add_book_empty_fields(self):
        # Негативный тест - пустое поле
        with self.assertRaises(ValueError):
            self.manager.add_book("1984", "", "Антиутопия", "328")

    def test_add_book_invalid_pages(self):
        # Негативный тест - некорректные страницы
        with self.assertRaises(ValueError):
            self.manager.add_book("1984", "Оруэлл", "Фантастика", "abc")

    def test_filter_by_pages(self):
        # Граничные и позитивные тесты
        self.manager.add_book("Книга 1", "Автор", "Жанр", "150")
        self.manager.add_book("Книга 2", "Автор", "Жанр", "250")
        
        filtered = self.manager.filter_by_pages(200)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['title'], "Книга 2")

if __name__ == "__main__":
    unittest.main()