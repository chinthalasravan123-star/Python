from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional


class Book:
    def __init__(self, title: str, author: str, isbn: str, available: bool = True) -> None:
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "available": self.available,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            available=data.get("available", True),
        )


class LibrarySystem:
    def __init__(self, data_file: Optional[str] = None) -> None:
        self.data_file = Path(data_file or Path(__file__).with_name("library_data.json"))
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        if not self.data_file.exists():
            self.books = []
            return

        try:
            with self.data_file.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            self.books = [Book.from_dict(item) for item in data]
        except (json.JSONDecodeError, OSError):
            self.books = []

    def save_books(self) -> None:
        with self.data_file.open("w", encoding="utf-8") as handle:
            json.dump([book.to_dict() for book in self.books], handle, indent=2)

    def add_book(self, title: str, author: str, isbn: str) -> Book:
        if self.get_book_by_isbn(isbn):
            raise ValueError("A book with this ISBN already exists.")

        book = Book(title=title, author=author, isbn=isbn)
        self.books.append(book)
        self.save_books()
        return book

    def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        for book in self.books:
            if book.isbn.lower() == isbn.lower():
                return book
        return None

    def search_books(self, query: str) -> List[Book]:
        query = query.lower()
        return [
            book
            for book in self.books
            if query in book.title.lower() or query in book.author.lower() or query in book.isbn.lower()
        ]

    def list_books(self) -> List[Book]:
        return self.books

    def borrow_book(self, isbn: str) -> Book:
        book = self.get_book_by_isbn(isbn)
        if not book:
            raise ValueError("Book not found.")
        if not book.available:
            raise ValueError("Book is already borrowed.")

        book.available = False
        self.save_books()
        return book

    def return_book(self, isbn: str) -> Book:
        book = self.get_book_by_isbn(isbn)
        if not book:
            raise ValueError("Book not found.")
        if book.available:
            raise ValueError("Book is already available.")

        book.available = True
        self.save_books()
        return book

    def remove_book(self, isbn: str) -> None:
        book = self.get_book_by_isbn(isbn)
        if not book:
            raise ValueError("Book not found.")

        self.books.remove(book)
        self.save_books()

    def get_stats(self) -> dict:
        total = len(self.books)
        available = sum(1 for book in self.books if book.available)
        borrowed = total - available
        return {"total": total, "available": available, "borrowed": borrowed}


def print_menu() -> None:
    print("\nLibrary Management System")
    print("1. Add a book")
    print("2. List all books")
    print("3. Search books")
    print("4. Borrow a book")
    print("5. Return a book")
    print("6. Remove a book")
    print("7. Show statistics")
    print("8. Exit")


def prompt(text: str) -> str:
    return input(text).strip()


def print_books(books: List[Book]) -> None:
    if not books:
        print("No books found.")
        return

    for book in books:
        status = "Available" if book.available else "Borrowed"
        print(f"- {book.title} by {book.author} | ISBN: {book.isbn} | Status: {status}")


def main() -> None:
    library = LibrarySystem()

    while True:
        print_menu()
        choice = prompt("Choose an option: ")

        if choice == "1":
            title = prompt("Enter title: ")
            author = prompt("Enter author: ")
            isbn = prompt("Enter ISBN: ")
            try:
                library.add_book(title, author, isbn)
                print("Book added successfully.")
            except ValueError as exc:
                print(f"Error: {exc}")

        elif choice == "2":
            print_books(library.list_books())

        elif choice == "3":
            query = prompt("Enter search term: ")
            print_books(library.search_books(query))

        elif choice == "4":
            isbn = prompt("Enter ISBN to borrow: ")
            try:
                library.borrow_book(isbn)
                print("Book borrowed successfully.")
            except ValueError as exc:
                print(f"Error: {exc}")

        elif choice == "5":
            isbn = prompt("Enter ISBN to return: ")
            try:
                library.return_book(isbn)
                print("Book returned successfully.")
            except ValueError as exc:
                print(f"Error: {exc}")

        elif choice == "6":
            isbn = prompt("Enter ISBN to remove: ")
            try:
                library.remove_book(isbn)
                print("Book removed successfully.")
            except ValueError as exc:
                print(f"Error: {exc}")

        elif choice == "7":
            stats = library.get_stats()
            print(f"Total books: {stats['total']}")
            print(f"Available books: {stats['available']}")
            print(f"Borrowed books: {stats['borrowed']}")

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
