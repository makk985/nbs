# NBS Project

## Description

NBS is a Django-based web application designed to manage user accounts, orders, payments, and products. It integrates with Google for authentication and provides a robust framework for handling various e-commerce functionalities.

## Features

- User authentication and management
- Order processing
- Payment integration
- Product catalog
- Media file handling
- Google OAuth2 authentication

## Requirements

- Python 3.8 or higher
- Django 5.1.4
- Other dependencies as specified in `requirements.txt`

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/nbs.git
   cd nbs
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**

   Create a `.env` file in the root directory and add the following variables:

   ```
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   DEBUG=True
   ```

6. **Run database migrations:**

   ```bash
   python manage.py migrate
   ```

7. **Create a superuser (optional):**

   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

## Usage

- Access the application at `http://127.0.0.1:8000/`.
- Use the admin panel at `http://127.0.0.1:8000/admin/` to manage users, orders, and products.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django documentation for guidance on best practices.
- Allauth for user authentication.