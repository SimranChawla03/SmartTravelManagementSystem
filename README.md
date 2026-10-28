# Smart Travel Management System (STMS)

A web-based travel management application that allows users to search travel options, select flights, calculate fares, make bookings, and manage their booking history.

**Live Website:** https://smarttravelmanagementsystem.onrender.com

**GitHub Repository:** https://github.com/SimranChawla03/SmartTravelManagementSystem

---

## 📌 Project Overview

The **Smart Travel Management System (STMS)** is designed to simplify the travel-booking workflow through a centralized web application. Users can register, log in, explore travel options, select flights, calculate booking costs, receive booking confirmation details, and view their previous bookings.

The project demonstrates full-stack web development, database integration, user authentication, booking management, version control, and cloud deployment.

## 🎯 Objectives

- Provide a simple interface for searching travel options.
- Implement user registration and authentication.
- Allow users to select flight options and calculate fares.
- Store and manage booking details in a database.
- Display booking confirmation and booking history.
- Apply software project management and testing practices using Jira.

## ✨ Key Features

- **User Registration:** Create a user account with input validation.
- **User Login and Logout:** Authenticate users and manage sessions.
- **Destination Search:** Search for travel options using the available search functionality.
- **Flight Selection:** View and select displayed flight options.
- **Fare Calculation:** Calculate and display the booking total.
- **Booking Management:** Submit bookings and store booking details.
- **Booking Confirmation:** Display booking confirmation information and a reference.
- **My Bookings:** View previously saved bookings.
- **Access Control:** Restrict booking-history access to authenticated users.

## 🧩 Main Modules

### Module 1: User Registration and Login
- User registration and input validation
- Login and logout
- Authentication and session management

### Module 2: Travel Search and Booking
- Destination search and travel options
- Flight selection
- Fare calculation
- Booking submission and storage
- Booking confirmation and booking history

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| HTML | Web page structure |
| CSS | Styling and layout |
| JavaScript | Frontend interactions |
| Python | Backend programming |
| Flask | Web framework and application routes |
| MongoDB Atlas | Cloud database |
| PyMongo | Python–MongoDB integration |
| Git | Version control |
| GitHub | Source-code hosting |
| Jira | Project management and task tracking |
| Render | Application deployment |
| Gunicorn | Python application server |

## 🏗️ System Architecture

The application follows a client-server architecture.

1. **Frontend:** HTML, CSS, and JavaScript provide the user interface.
2. **Backend:** Flask processes requests, validates inputs, manages sessions, and handles application logic.
3. **Database:** MongoDB Atlas stores application data, including user and booking information.
4. **Deployment:** The application is hosted on Render and served using Gunicorn.

## 📋 Project Management with Jira

Jira was used to organize development work into six epics:

1. User Authentication and Security
2. Destination Search and Selection
3. Flight Options and Fare Calculation
4. Booking Management and Confirmation
5. My Bookings and Booking History
6. Testing, Bug Tracking and Release

Stories, tasks, subtasks, and a sprint were used to organize and track project activities.

## 🧪 Testing

Test cases were prepared to cover:

- Registration and login
- Destination search and flight selection
- Fare calculation and booking submission
- Booking confirmation and booking history
- Input validation and negative scenarios
- Integration, security, regression, and end-to-end testing

Actual results and test statuses should be recorded after executing the corresponding test cases.

## 🚀 Run the Project Locally

### Prerequisites

- Python installed
- Git installed
- A MongoDB Atlas account and database connection string

### Step 1: Clone the repository

```bash
git clone https://github.com/SimranChawla03/SmartTravelManagementSystem.git
```

### Step 2: Open the project directory

```bash
cd SmartTravelManagementSystem
```

### Step 3: Create and activate a virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

### Step 4: Install dependencies

If the repository contains `requirements.txt`, run:

```bash
pip install -r requirements.txt
```

### Step 5: Configure environment variables

Create a local `.env` file if required by the application and configure the variables expected by the code.

Example:

```env
SECRET_KEY=your_secret_key
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=your_database_name
```

Replace the example values with your actual configuration. Never commit real passwords, database credentials, or secret keys to GitHub.

### Step 6: Start the application

If `app.py` contains the Flask application and its development entry point, run:

```bash
python app.py
```

Open the local URL displayed in the terminal, commonly:

```text
http://127.0.0.1:5000
```

## ☁️ Deployment

The application is deployed using Render.

**Live URL:** https://smarttravelmanagementsystem.onrender.com

The source code is maintained in GitHub, and the deployed application uses environment variables for configuration.

## 🔮 Future Enhancements

- Integration with real-time flight search APIs
- Online payment gateway integration
- Email notifications and booking updates
- Improved error handling and monitoring
- Additional security and automated testing
- Enhanced travel recommendations

## 👩‍💻 Author

**Simran Chawla**

B.Tech — Computer Science

**GitHub:** https://github.com/SimranChawla03

---

*Smart Travel Management System — simplifying the travel-booking workflow through web technology.*
