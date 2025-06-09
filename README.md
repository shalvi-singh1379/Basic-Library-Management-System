# 📚 Basic Library Management System

This is a simple **Library Management System** implemented in Python using **SQLite3**. It provides a command-line interface to manage books and users, allowing functionalities such as adding/removing/searching books, issuing/returning books, and managing user data.

---

## 🔧 Features

- ✅ Add, search, display, and remove books  
- ✅ Add and list users (Student, Faculty, Admin)  
- ✅ Issue and return books with stock updates  
- ✅ SQLite-based persistent database  
- ✅ CLI-based interaction for ease of use  
- ✅ Auto-creation and population of database tables on first run  

---

## 🗂️ Folder Structure

```bash
library_management/
│
├── library.py       # Main script with Library, Book, User classes and logic
└── library.db       # SQLite database (auto-generated on first run)
```
# 💻 How to Run

### Clone the Repository

```bash
git clone https://github.com/your-username/library-management-system.git
cd library-management-system
```

### Run the Program

```bash
python library.py
```

### Follow the Menu Prompts

```
Library Management System
1. Add Book
2. Remove Book
3. Search Book
...
```

---

## 🛠️ Technologies Used

- Python 3  
- SQLite3 (built-in database module)

---

## 🧠 Example Functionalities

- Add a new book with a unique `book_id`  
- Issue a book to a user only if copies are available  
- Return a book and update the available stock  
- Auto-insert sample books and users on first run  

---

## 📌 Future Improvements

- Add GUI support (Tkinter or Flask)  
- Maintain issue/return history  
- User login system with permissions  
- Due date and fine management  

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
