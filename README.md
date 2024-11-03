# Personal Finance Tracker

A web-based application to help users manage and track their personal finances. Users can view financial history, change settings, and securely log in or register.

## Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Technologies](#technologies)
- [Contributing](#contributing)
- [License](#license)

## Features
- **User Authentication**: Secure login, registration, and password management.
- **Track Financial History**: View detailed financial transactions and records.
- **Responsive Design**: Accessible on both desktop and mobile devices.
- **Notifications**: Alerts for important account changes or errors.

## Demo
A live demo of the project can be accessed here: [Demo URL]([#](https://youtu.be/3mp9Y-d6idE))

## Installation

### Prerequisites
- Python 3.8+
- Flask
- A PostgreSQL (or alternative SQL database) setup

### Steps
1. **Clone the repository**:
    ```bash
    git clone https://github.com/HTIMASI/CS50_final_project/personal-finance-tracker.git
    cd personal-finance-tracker
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:
   - Create a database for the project in your database system (e.g., PostgreSQL).
   - Update the database URL in the configuration file.

5. **Run the application**:
    ```bash
    flask run
    ```

6. **Access the application**:
   - Open a web browser and go to `http://127.0.0.1:5000`

## Usage

Once the app is running, users can:
1. **Register**: Create a new account to start tracking finances.
2. **Login**: Access personal financial records securely.
3. **View History**: Navigate to the history section to see past transactions.
4. **Update Account**: Change password and other settings via the account settings.

### Navigation
- **Home**: Main dashboard with an overview of finances.
- **History**: Detailed financial transaction records.
- **Change Password**: Update password securely.
- **Login/Register**: Login for existing users, register for new users.

## Configuration

Update `config.py` or use environment variables to configure the following:
- **Database URL**: Define your SQL database connection string.
- **Google Analytics ID**: For tracking user activity (optional).
- **Secret Key**: Used by Flask for session management and CSRF protection.


## Technologies
**Backend**: Flask, Jinja2
**Frontend**: Bootstrap, HTML, CSS, JavaScript, Font Awesome
**Database**: PostgreSQL (or your preferred SQL database)
**Scripts**: JQuery, Google Analytics

## Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new feature branch (git checkout -b feature-branch-name).
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature-branch-name).
Open a Pull Request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
