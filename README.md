# Personal Website - Flask

![image](https://github.com/user-attachments/assets/fc1ecc7d-c44e-462a-b536-d37b2a90d328)

## 🚀 Overview
This is my **personal portfolio website**, built using **Flask**. It serves as a digital resume, showcasing my projects, technical skills, and a blog section. It is fully responsive, secure, and designed for easy deployment.

## ✨ Features
- **Home Page** - Introduction and personal branding.
- **Projects Showcase** - Displays my best work with descriptions and links.
- **Blog Section** - Articles about AI, Python, and software development.
- **Comment Section** - Users can comment on every blog post.
- **Contact Form** - Users can send me messages directly.
- **Admin Panel** - Secure admin dashboard for managing blog posts.
- **Mobile-Friendly** - Fully responsive design.
- **Password Hashing** - Secure user authentication using Flask-Login.
- **Deployment** - Easily deployed to Heroku with Gunicorn.
- **Database Integration** - Uses PostgreSQL (or SQLite for local development).
- **Responsiveness** - Works seamlessly across all devices.
- **Environment Variables** - Securely stores sensitive data using `.env` or Heroku config vars.
- **SEO Optimization** - Enhanced for better search engine ranking.

## 🛠️ Tech Stack
- **Backend:** Flask, Python
- **Frontend:** HTML, CSS, JavaScript
- **Database:** PostgreSQL (or SQLite for local development)
- **Styling:** Bootstrap, Custom CSS
- **Authentication:** Flask-Login (for admin panel security)
- **Deployment:** Heroku (with Gunicorn)

## 🔧 Installation & Setup
To run this project locally:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/dawidk-website.git
   cd dawidk-website
   ```

2. **Create a Virtual Environment & Install Dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export SECRET_KEY='your-secret-key'
   ```
   *(Use a `.env` file for better security when handling secrets)*

4. **Run the Application**
   ```bash
   flask run
   ```

5. **Access the Website**
   - Open `http://127.0.0.1:5000/` in your browser.

## 🚀 Deployment to Heroku
1. **Login to Heroku & Create App**
   ```bash
   heroku login
   heroku create my-portfolio-website
   ```
2. **Push Code to Heroku**
   ```bash
   git push heroku main
   ```
3. **Set Up Environment Variables on Heroku**
   ```bash
   heroku config:set SECRET_KEY='your-secret-key'
   ```
4. **Open Your Deployed Website**
   ```bash
   heroku open
   ```

## 🎯 Future Improvements
- Add more animations for better UX.
- Implement a CMS-like backend for easy blog post management.
- Improve SEO for better visibility.
- Make a functional contact form.
- Interactive ML portfolio section.
- Dark Mode - User-friendly dark/light theme toggle.

