# FoodLink - Food Donation Management System

FoodLink is a web application that connects food donors with delivery personnel and recipient organizations to reduce food waste and fight hunger. The application allows donors to donate excess food, delivery personnel to transport the food, and administrators to manage the entire process.

## Features

### For Donors
- Register and login as a donor
- Add new food donations with details (food type, quantity, freshness, pickup location)
- Track donation status (pending, assigned, in transit, delivered)
- View donation history and impact

### For Delivery Personnel
- Register and login as a delivery person
- View assigned deliveries
- Update delivery status (assigned, on the way, picked up, delivered)
- Provide delivery confirmation (signature, photo, feedback)

### For Administrators
- Login as an admin
- View pending donations and assign delivery personnel
- Manage recipient organizations
- Track overall statistics (total donations, delivered food, active riders)

## Technology Stack

- **Backend**: Python with Flask framework
- **Database**: SQLAlchemy ORM with SQLite database
- **Frontend**: HTML, CSS, Bootstrap 4, JavaScript
- **Authentication**: Flask-Login

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository or download the source code

2. Navigate to the project directory
   ```
   cd TraeFWD
   ```

3. Create a virtual environment (optional but recommended)
   ```
   python -m venv venv
   ```

4. Activate the virtual environment
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required packages
   ```
   pip install -r requirements.txt
   ```

6. Create a `.env` file in the project root with the following content:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///foodforward.db
   ```

7. Initialize the database
   ```
   python app.py
   ```

8. Access the application
   - Open your web browser and go to `http://127.0.0.1:5000`

## Usage

### Initial Setup

1. Register as an admin user
2. Add recipient organizations through the admin dashboard
3. Register as donors and delivery personnel

### Workflow

1. Donors add new food donations
2. Admins assign delivery personnel to pending donations
3. Delivery personnel update the status as they pick up and deliver the food
4. Admins track the overall process and manage the system

## Project Structure

- `app.py`: Main application file
- `models.py`: Database models
- `forms.py`: Form definitions
- `routes.py`: Route definitions
- `templates/`: HTML templates
- `static/`: Static files (CSS, JavaScript)

## License

This project is licensed under the MIT License.