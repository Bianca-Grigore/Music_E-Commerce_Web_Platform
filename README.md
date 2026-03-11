# 🎵 Premium Music Store E-Commerce Platform

A fully-featured, modern e-commerce web application built with **Django**. This platform is designed for a music store (selling CDs, vinyl, instruments, etc.) and features a custom-built **Premium Dark Mode UI**, advanced product filtering, secure user authentication, and a dynamic frontend shopping cart.

## ✨ Key Features

### 🎨 Modern UI/UX (Premium Dark Theme)
* **Custom Dark Mode:** Built from scratch using modern CSS, featuring glassmorphism effects, neon accents (Spotify Green / Purple), and sleek hover animations.
* **Responsive Grid Layouts:** Products, forms, and profile dashboards are structured using CSS Grid and Flexbox for seamless scaling on mobile and desktop.
* **Dynamic Navbar:** Sticky header with dropdown menus, conditional rendering based on user authentication, and role-based admin links.
* **Animated Promo Banners:** JavaScript-driven animated banners for secret offers.

### 🛍️ Product Management & Shopping
* **Advanced Filtering & Sorting:** Users can filter products by category, price range, stock levels, promotional campaigns, and addition dates. 
* **Frontend Cart System:** "Add to Cart" functionality built with Vanilla JavaScript and `localStorage` for a blazing-fast, page-reload-free user experience.
* **Pagination:** Built-in Django pagination with custom-styled navigation buttons.

### 🔐 Security & User Authentication
* **Custom Registration & Login:** Extended Django `UserCreationForm` to include detailed profile information (Phone, Country, County, City, Street).
* **Profile Dashboard:** A personalized control panel for users to view their session data and manage their accounts.
* **Role-Based Access Control (RBAC):** "Add Product", "Log", and "Info" buttons are exclusively visible to users in the `Administratori_site` group or those with specific permissions.

### ⚙️ Advanced Backend Form Validations
The application features complex, custom backend validations to ensure data integrity:
* **Product Pricing Logic:** Ensures minimum markup percentages (e.g., minimum 20% markup for products over 1000 RON).
* **Contact Form:** Validates exact Romanian CNP formats, calculates age from CNP (must be 18+), restricts temporary email domains, checks word counts, and enforces capitalization rules.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.x, Django 5.x
* **Frontend:** HTML5, CSS3 (Custom Dark Theme), Vanilla JavaScript, Bootstrap 5 (Grid baseline)
* **Database:** SQLite (default) / PostgreSQL (production ready)
