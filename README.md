# Advanced-Database-Systems-Design

Here’s a professional and informative **project description** for your GitHub repository titled **"Vindhu Bhojanam"**:

---

## 🍛 Vindhu Bhojanam - Restaurant Ordering Web App

**Vindhu Bhojanam** is a full-stack restaurant web application built using **Flask (Python)**, **HTML/CSS**, **Bootstrap**, and **SQLite**. It offers users a seamless and culturally enriched food-ordering experience inspired by traditional South Indian cuisine.

### 🚀 Features

* 🔐 **User Authentication**: Secure signup, login, and logout functionalities.
* 🧾 **Interactive Menu**: Dynamic category-wise food menu including *Starters, Biryani, Main Course, Desserts, and Beverages*.
* 🛒 **Cart System**:

  * Add items to cart with quantity control.
  * View and update cart in real-time.
  * Checkout with session-based order tracking.
* 📋 **Order Management**:

  * Orders are stored in a persistent SQLite database.
  * Users can view their current cart and finalize orders.
* 🧠 **Admin Interface**:

  * Add new menu items along with image, description, and optional nutrition details.
* 🌐 **Cultural UI**:

  * Telugu typography and local icons included for regional flavor.
  * Fully responsive design using Bootstrap.

### ⚙️ Tech Stack

* **Backend**: Python, Flask
* **Frontend**: HTML5, CSS3, Bootstrap 5
* **Database**: SQLite
* **Templating**: Jinja2

### 📂 Folder Structure

```
.
├── app.py                  # Main Flask application
├── templates/              # Jinja2 HTML templates
│   ├── menu/               # Menu category pages
│   └── *.html              # Layout and route templates
├── static/                 # Images, CSS, logos
├── restaurant.db           # SQLite database
├── requirements.txt        # Dependencies
```

### 🔧 Setup Instructions

1. Clone this repo:

   ```bash
   git clone https://github.com/yourusername/vindhu-bhojanam.git
   cd vindhu-bhojanam
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:

   ```bash
   python app.py
   ```
4. Open `http://127.0.0.1:5000` in your browser.

---

Would you like me to create a `README.md` file for this automatically?
