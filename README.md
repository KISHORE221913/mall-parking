# 🚗 Mall Parking Management System

The Mall Parking Management System is a full-stack web application developed using Django that automates and simplifies vehicle parking operations in a multi-floor mall environment. The system is designed to efficiently manage vehicle entry, slot allocation, billing, and exit processes while providing a smooth and user-friendly experience.

This application allows users to register vehicle entry details such as vehicle number, type (car/bike), VIP status, and email. Based on these inputs, the system automatically assigns an available parking slot and floor using a smart allocation algorithm. Each vehicle is given a unique ticket ID, and entry time is recorded for billing purposes.

The system includes a dynamic billing feature where the total parking cost is calculated based on the duration of stay. VIP and regular vehicles have different pricing rules. Upon successful entry, a parking ticket is generated and sent to the user's email using SendGrid email API integration.

An admin login system is implemented to ensure secure access. After logging in, the admin can access features such as the dashboard, parking slots visualization, vehicle entry/exit management, and billing details. The dashboard provides real-time statistics such as the number of cars, bikes, and VIP vehicles parked on a given day.

The project is deployed on the cloud using Render and uses PostgreSQL as the backend database. All sensitive data such as database credentials and API keys are securely managed using environment variables.

---

## 🌐 Live Website

https://mall-parking-tm7p.onrender.com

---

## 🔐 Admin Login Credentials

Username: `parkingadmin`  
Password: `parking123`  

---

## 🗄️ Database Access

The project uses a cloud-based PostgreSQL database hosted on Render.  
Direct public access to the database is restricted for security reasons.

However, the data can be viewed using:

- Django Admin Panel:  
  https://mall-parking-tm7p.onrender.com/admin/

- Or via Render Dashboard using the External Database URL.

---

## 📧 Email Notification

- The system sends a parking ticket to the user's email after vehicle entry.
- Email is integrated using SendGrid API.
- ⚠️ Note: The email may appear in the **Spam folder** initially due to sender authentication and free-tier limitations.

---

## 🛠️ Technologies Used

- Backend: Django (Python)
- Frontend: HTML, CSS
- Database: PostgreSQL (Render Cloud)
- Deployment: Render
- Email Service: SendGrid API

---

## 🚀 Key Features

- Smart parking slot allocation (Car, Bike, VIP)
- Multi-floor parking management
- Automatic billing based on time
- Unique ticket generation
- Email notification system
- Admin authentication and dashboard
- Real-time parking slot visualization

---

## 🔐 Security

All sensitive information such as API keys and database URLs are stored using environment variables and are not exposed in the source code.

---

## 📌 Conclusion

This project demonstrates a real-world implementation of a parking management system using Django, showcasing backend logic, cloud deployment, database integration, and email services. It is scalable and can be extended with features like online payments, QR code entry, and mobile application integration.

---
