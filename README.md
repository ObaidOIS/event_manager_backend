# Django Project with Function-Based Views and DRF APIs

This Django project includes a set of APIs built with Django Rest Framework (DRF) and utilizes function-based views (FBVs). It features the ability to send email invitations to users, with credentials managed via environment variables.

## Table of Contents

- [Project Setup](#project-setup)
- [Running the Application](#running-the-application)
- [Feature Implementation](#feature-implementation)
- [Assumptions](#assumptions)

## Project Setup

### Prerequisites

- Python 3.8
- Django 5.0
- Django Rest Framework
- Email SMTP service credentials

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/obaidois/event_manager_backend.git
    cd event_manager_backend
    ```

2. Create a virtual environment and activate it:
    ```bash
    python virtual venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables. Create a `.env` file in the project root:
    ```dotenv

    SECRET_KEY= ''
    ALLOWED_HOSTS=*
    CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST='smtp.gmail.com'
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=your_email@example.com
    EMAIL_HOST_PASSWORD=your_password
    ```

5. Run migrations to set up the database:
    ```bash
    python manage.py migrate
    ```

6. Create a superuser (optional but recommended):
    ```bash
    python manage.py createsuperuser
    ```

## Running the Application

1. Start the Django development server:
    ```bash
    python manage.py runserver
    ```

2. Access the API at `http://127.0.0.1:8000/api/`.


- **Function-Based Views:**
- Used for handling standard HTTP requests in the `views.py` file within the `invitations` app.

- **DRF APIs:**
- Used for creating RESTful endpoints, defined in the `urls.py` and `views.py` files of the `invitations` app.

- **Email Invitation:**
- Email functionality is managed using Django's built-in `send_mail` function, with credentials stored in environment variables.

## Feature Implementation

### Sending Invitations via Email

The feature to send email invitations is implemented using Django's `send_mail` function. An invitation email is sent to a user when their details are submitted via a form or API endpoint.

#### Steps:

1. Collect email details from the user.
2. Use the `send_mail` function to send an email.
3. The email template is located in `invitations/templates/invitations/email_template.html`.

### Incomplete Requirements Approach

For the email invitation feature, where specific requirements were incomplete, the following approach was taken:

- A generic email template was used for simplicity.
- The system assumes valid SMTP credentials are provided in the environment variables.
- Additional features like invitation token generation and acceptance tracking can be added if required.

## Assumptions

- Valid SMTP server credentials will be provided via environment variables.
- Email templates will be simple HTML files.
- The Django app will be run in a development environment using `python manage.py runserver`.

For further customization or deployment, additional configurations may be required.
