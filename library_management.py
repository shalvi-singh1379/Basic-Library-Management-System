import sqlite3

class Book:
    def __init__(self, book_id, book_name, author, copies):
        self.book_id = book_id
        self.book_name = book_name
        self.author = author
        self.copies = copies

    def __str__(self):
        return f"Book ID: {self.book_id}, Name: {self.book_name}, Author: {self.author}, Copies: {self.copies}"


class User:
    def __init__(self, user_id, user_name, role):
        self.user_id = user_id
        self.user_name = user_name
        self.role = role

    def __str__(self):
        return f"User ID: {self.user_id}, Name: {self.user_name}, Role: {self.role}"


class Library:
    def __init__(self, db_name='library.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS books (
                book_id TEXT PRIMARY KEY,
                book_name TEXT NOT NULL,
                author TEXT NOT NULL,
                copies INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                user_name TEXT NOT NULL,
                role TEXT NOT NULL
            );

            INSERT INTO books (book_id, book_name, author, copies) VALUES
            ('B001', 'To Kill a Mockingbird', 'Harper Lee', 5),
            ('B002', '1984', 'George Orwell', 8),
            ('B003', 'The Great Gatsby', 'F. Scott Fitzgerald', 4),
            ('B004', 'The Catcher in the Rye', 'J.D. Salinger', 6),
            ('B005', 'Moby-Dick', 'Herman Melville', 3),
            ('B006', 'Pride and Prejudice', 'Jane Austen', 7),
            ('B007', 'War and Peace', 'Leo Tolstoy', 2),
            ('B008', 'The Odyssey', 'Homer', 10),
            ('B009', 'Ulysses', 'James Joyce', 1),
            ('B010', 'Madame Bovary', 'Gustave Flaubert', 5),
            ('B011', 'The Divine Comedy', 'Dante Alighieri', 4),
            ('B012', 'Hamlet', 'William Shakespeare', 9),
            ('B013', 'The Hobbit', 'J.R.R. Tolkien', 8),
            ('B014', 'Crime and Punishment', 'Fyodor Dostoevsky', 6),
            ('B015', 'The Brothers Karamazov', 'Fyodor Dostoevsky', 3)
            ON CONFLICT(book_id) DO NOTHING;

            INSERT INTO users (user_id, user_name, role) VALUES
            ('U001', 'Alice Johnson', 'Student'),
            ('U002', 'Bob Smith', 'Faculty'),
            ('U003', 'Charlie Brown', 'Admin'),
            ('U004', 'David Wilson', 'Student'),
            ('U005', 'Eva Green', 'Faculty')
            ON CONFLICT(user_id) DO NOTHING;
        ''')
        self.conn.commit()

    def add_book(self, book_id, book_name, author, copies):
        self.cursor.execute('''
            INSERT INTO books (book_id, book_name, author, copies)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(book_id) DO UPDATE SET
                copies = copies + excluded.copies
        ''', (book_id, book_name, author, copies))
        self.conn.commit()
        print(f"Book '{book_name}' added successfully!")

    def remove_book(self, book_id):
        self.cursor.execute('DELETE FROM books WHERE book_id = ?', (book_id,))
        self.conn.commit()
        if self.cursor.rowcount > 0:
            print("Book removed successfully!")
        else:
            print("Book not found!")

    def search_book(self, book_id):
        self.cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
        book = self.cursor.fetchone()
        if book:
            print(Book(*book))
        else:
            print("Book not found!")

    def display_books(self):
        self.cursor.execute('SELECT * FROM books')
        books = self.cursor.fetchall()
        print("\nBooks in the Library:")
        for book in books:
            print(Book(*book))

    def display_users(self):
        self.cursor.execute('SELECT * FROM users')
        users = self.cursor.fetchall()
        print("\nUsers in the Library:")
        for user in users:
            print(User(*user))

    def issue_book(self, user_id, book_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = self.cursor.fetchone()
        if user:
            self.cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
            book = self.cursor.fetchone()
            if book:
                if book[3] > 0:
                    self.cursor.execute('UPDATE books SET copies = copies - 1 WHERE book_id = ?', (book_id,))
                    self.conn.commit()
                    print(f"Book '{book[1]}' issued to user '{user[1]}'")
                else:
                    print("No copies available for this book!")
            else:
                print("Book not found!")
        else:
            print("User not found!")

    def return_book(self, user_id, book_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = self.cursor.fetchone()
        if user:
            self.cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
            book = self.cursor.fetchone()
            if book:
                self.cursor.execute('UPDATE books SET copies = copies + 1 WHERE book_id = ?', (book_id,))
                self.conn.commit()
                print(f"Book '{book[1]}' returned by user '{user[1]}'")
            else:
                print("Book not found!")
        else:
            print("User not found!")

    def add_user(self, user_id, user_name, role):
        self.cursor.execute('''
            INSERT INTO users (user_id, user_name, role)
            VALUES (?, ?, ?)
        ''', (user_id, user_name, role))
        self.conn.commit()
        print(f"User '{user_name}' added successfully!")

    def __del__(self):
        self.conn.close()


def main():
    library = Library()

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Search Book")
        print("4. Display Books")
        print("5. Display Users")
        print("6. Issue Book")
        print("7. Return Book")
        print("8. Add User")
        print("9. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            book_id = input("Enter book ID: ")
            book_name = input("Enter book name: ")
            author = input("Enter author name: ")
            copies = int(input("Enter number of copies: "))
            library.add_book(book_id, book_name, author, copies)
        elif choice == '2':
            book_id = input("Enter book ID to remove: ")
            library.remove_book(book_id)
        elif choice == '3':
            book_id = input("Enter book ID to search: ")
            library.search_book(book_id)
        elif choice == '4':
            library.display_books()
        elif choice == '5':
            library.display_users()
        elif choice == '6':
            user_id = input("Enter user ID: ")
            book_id = input("Enter book ID to issue: ")
            library.issue_book(user_id, book_id)
        elif choice == '7':
            user_id = input("Enter user ID: ")
            book_id = input("Enter book ID to return: ")
            library.return_book(user_id, book_id)
        elif choice == '8':
            user_id = input("Enter user ID: ")
            user_name = input("Enter user name: ")
            role = input("Enter user role (Student/Faculty/Admin): ")
            library.add_user(user_id, user_name, role)
        elif choice == '9':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice! Please enter a valid option.")


if __name__ == "__main__":
    main()
