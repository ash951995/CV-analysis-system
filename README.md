# CV Analysis Chatbot

This project is a Flask-based web application that allows users to upload CVs (in PDF or DOCX format), parse the content, analyze the CV using an LLM (Large Language Model), and then interact with the CV data through a chatbot interface.

## Features

* **CV Upload:** Users can upload CV files in PDF or DOCX format.
* **CV Parsing:** The application extracts text from the uploaded CVs using OCR (for PDFs) and direct text extraction (for DOCX).
* **LLM Analysis:** The extracted text is sent to an LLM (e.g., using OpenAI's API or a local LLM), which analyzes the CV and extracts structured data (personal information, education, experience, skills, etc.).
* **Database Storage:** The extracted structured data is stored in a PostgreSQL database using SQLAlchemy.
* **Chatbot Interface:** Users can interact with the CV data through a chatbot interface, asking questions about the candidate's information.

## Technologies Used

* **Flask:** Web framework for building the application.
* **Python:** Programming language.
* **PostgreSQL:** Database for storing CV data.
* **SQLAlchemy:** ORM (Object-Relational Mapper) for database interactions.
* **pdf2image:** Library for converting PDF pages to images.
* **PyTesseract:** OCR engine for extracting text from images.
* **python-docx:** Library for extracting text from DOCX files.
* **TOGETHER API (or similar):** LLM for CV analysis.
* **JavaScript (Fetch API):** Client side scripting for API calls.
* **HTML/CSS:** Frontend.
* **Docker & Docker Compose:** Containerization and orchestration.
* **Flask-Cors:** Cross Origin Resource Sharing.

## Setup Instructions

1.  **Clone the Repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**

    * Create a `.env` file in the root directory of the project.
    * Add the following environment variables, replacing the placeholders with your actual values:

        ```
        
        DATABASE_URL=postgresql://your_postgres_user:your_postgres_password@db:5432/your_postgres_db
        POSTGRES_USER=your_postgres_user
        POSTGRES_PASSWORD=your_postgres_password
        POSTGRES_DB=your_postgres_db
        TOGETHER_API_URL="your_together_api_url" #if using together ai
        API_KEY=your_together_api_key #if using together ai
        ```

5.  **Run with Docker Compose (Recommended):**

    ```bash
    docker-compose up --build
    ```

6.  **Run Locally (Without Docker):**

    * Ensure you have PostgreSQL installed and running.
    * Initialize the database:

        ```bash
        python app.py  # or python __init__.py if app.py calls create_app()
        ```

    * Run the Flask application:

        ```bash
        python app.py
        ```

7.  **Access the Application:**

    * Open your web browser and go to `http://127.0.0.1:5000/api/` (or `http://localhost:5000/api/`).

## Code Structure

* **`app.py` or `__init__.py`:** Main Flask application file.
* **`app/routes/upload_routes.py`:** Contains the Flask routes for uploading files and handling chatbot queries.
* **`app/parser/pdf_parser.py`:** Handles PDF parsing using OCR.
* **`app/parser/docx_parser.py`:** Handles DOCX parsing.
* **`app/llm_operations/llm.py`:** Contains the logic for interacting with the LLM for CV analysis.
* **`app/llm_operations/llm_query.py`:** Contains the logic for interacting with the LLM for chatbot queries.
* **`app/db_operations.py`:** Handles database operations using SQLAlchemy.
* **`templates/`:** Contains the HTML templates for the web interface.
* **`static/`:** Contains static files (CSS, JavaScript).
* **`uploads/`:** Directory where uploaded CVs are stored.
* **`docker-compose.yml`:** Docker Compose configuration file.
* **.env:** Environment variables.
* **.gitignore:** Git ignore file.

## Usage

1.  **Upload a CV:** Use the file upload form to upload a CV in PDF or DOCX format.
2.  **Chat with the CV:** Enter your questions in the chatbot input field and click "Send."

## LLM Interaction

* The application uses the OpenAI API (or a similar LLM) to analyze the CV and generate responses to user queries.
* You can customize the LLM prompts in `app/llm_operations/llm.py` and `app/llm_operations/llm_query.py` to improve the accuracy and relevance of the analysis and chatbot responses.

## Database Interaction

* The application uses SQLAlchemy to interact with a PostgreSQL database.
* The CV data is stored in the `cvs` table.
* You can modify the database schema and queries in `app/db_operations.py` to suit your needs.

## Docker

* The `docker-compose.yml` file provides a convenient way to run the application in a Docker container.
* The Docker setup includes a PostgreSQL database container.
* Environment variables are used to configure the application and database.

## Future Improvements

* Implement user authentication.
* Add more advanced CV analysis features.
* Improve the chatbot's natural language processing capabilities.
* Add more detailed error handling.
* Add unit and integration tests.
* Improve the frontend.
* Add support for more file types.