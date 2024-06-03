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
    git clone https://github.com/leAyush98/social_media_app.git
    cd social_media_app
    ```

2. **Create a `.env` file in the project root:**
    ```sh
    touch .env
    ```

    Add the following content to the `.env` file:
    ```env
    MYSQL_PASSWORD=your_mysql_password
    MYSQL_ROOT_PASSWORD=your_mysql_root_password
    ```

3. **Install Docker and Docker Compose:**
    - **Docker**: Follow the [official Docker installation guide](https://docs.docker.com/get-docker/).
    - **Docker Compose**: Follow the [official Docker Compose installation guide](https://docs.docker.com/compose/install/).


### Running the Application with Docker

1. **Build and start the containers:**
    ```sh
    docker-compose up -d --build
    ```

2. **Run the init_web file to make migrations, make sure to have necessary permissions :**
    ```sh
    ./init_web.sh
    ```

3. **Access the application:**
    Open your browser and navigate to `http://localhost:8000`.


### Postman Collection

Postman collection is provided in the parent folder. Import the collection into Postman and follow the included examples to interact with the API.

### Notes

- Ensure that the `.env` file is correctly configured with your database credentials.
- The application uses Docker Compose to manage the multi-container setup. Make sure Docker is running before executing the `docker-compose` commands.

By following these instructions, you should be able to set up and run the social media app with Docker and MySQL. If you encounter any issues, refer to the Docker and Django documentation for troubleshooting tips.
