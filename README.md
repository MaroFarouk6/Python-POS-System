# Python POS System (Point of Sale)

A full-featured, multi-threaded desktop Point of Sale (POS) application engineered from scratch using Python. Designed for a local business ("Al-Tahtawy Butchery"), this system manages inventory, sales, expenses, and administrative tasks with a secure, user-friendly GUI.

## 🌟 Key Features

### 🛒 Cashier Dashboard
* **Dynamic Item Grid:** Automatically generates button grids for items based on database categories.
* **Real-Time Basket:** Add/remove items, adjust quantities, and calculate totals instantly.
* **Transaction Management:** Supports sales, returns, and holding orders.
* **Temp Items:** Allows cashiers to add custom, non-inventory items on the fly.

### 🔐 Admin Panel (Secure)
* **Security:** SHA-256 hashing used for all password storage and authentication.
* **Inventory Management:** Full CRUD (Create, Read, Update, Delete) capabilities for items and categories.
* **Financial Analytics:** View daily bills, net profit, and expense reports.
* **User Management:** Admin controls for changing passwords and system settings.

## 🛠️ Technical Implementation

This project demonstrates a "full-stack" desktop architecture:

* **Language:** Python 3.x
* **GUI Framework:** `tkinter` & `ttk` (with `tksheet` for advanced data grids).
* **Database:** `sqlite3` relational database for persistent storage of transactions, inventory, and logs.
* **Concurrency:** Implemented `threading` to decouple database operations from the main UI thread, ensuring the interface never freezes during heavy queries.
* **Security:** `hashlib` implementation for secure credential management; strict hardware ID locking for license protection.

## 🚀 Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/MaroFarouk6/Python-POS-System.git](https://github.com/MaroFarouk6/Python-POS-System.git)
    cd Python-POS-System
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python app.py
    ```
    *(Default Admin Password: admin)*

## 📂 Project Structure

* `app.py`: The main application entry point and logic controller.
* `meat.db`: SQLite database file (generated automatically).
* `imgs/`: Directory containing UI assets and icons.

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---
**Developed by Omar (Mohamed Farouk) Amin**
*Connect with me on [LinkedIn](https://www.linkedin.com/in/omar-amin-1765342b5)*
