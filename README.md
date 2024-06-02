# Social Media App

A Django-based social media application with MySQL as the database, Docker for containerization, and Postman for API testing.

## Installation Instructions

### Prerequisites

- Python 3.9
- Docker and Docker Compose
- MySQL 5.7

### Environment Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/social-media-app.git
    cd social-media-app
    ```

2. **Create a `.env` file in the project root:**
    ```sh
    touch .env
    ```

    Add the following content to the `.env` file:
    ```env
    MYSQL_DATABASE=assignment
    MYSQL_USER=root
    MYSQL_PASSWORD=your_mysql_password
    MYSQL_ROOT_PASSWORD=your_mysql_root_password
    ```

3. **Install Docker and Docker Compose:**
    - **Docker**: Follow the [official Docker installation guide](https://docs.docker.com/get-docker/).
    - **Docker Compose**: Follow the [official Docker Compose installation guide](https://docs.docker.com/compose/install/).

### MySQL Installation (if not using Docker)

If you prefer to run MySQL locally instead of using Docker, follow these instructions:

1. **Install MySQL:**
    ```sh
    sudo apt-get update
    sudo apt-get install mysql-server
    ```

2. **Secure MySQL installation:**
    ```sh
    sudo mysql_secure_installation
    ```

3. **Create a database and user:**
    ```sql
    CREATE DATABASE assignment;
    CREATE USER 'root'@'localhost' IDENTIFIED BY 'your_mysql_password';
    GRANT ALL PRIVILEGES ON assignment.* TO 'root'@'localhost';
    FLUSH PRIVILEGES;
    ```

### Running the Application with Docker

1. **Build and start the containers:**
    ```sh
    docker-compose up --build
    ```

2. **Apply migrations and collect static files:**
    ```sh
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py collectstatic --noinput
    ```

3. **Access the application:**
    Open your browser and navigate to `http://localhost:8000`.

### Running the Application Locally

If you prefer not to use Docker, follow these instructions:

1. **Install Python dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

2. **Apply migrations and collect static files:**
    ```sh
    python manage.py migrate
    python manage.py collectstatic --noinput
    ```

3. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

4. **Access the application:**
    Open your browser and navigate to `http://localhost:8000`.

### Postman Collection

Use the provided Postman collection to test the API endpoints. Import the collection into Postman and follow the included examples to interact with the API.

### Notes

- Ensure that the `.env` file is correctly configured with your database credentials.
- The application uses Docker Compose to manage the multi-container setup. Make sure Docker is running before executing the `docker-compose` commands.

By following these instructions, you should be able to set up and run the social media app with Docker and MySQL. If you encounter any issues, refer to the Docker and Django documentation for troubleshooting tips.
