# AI-Powered Company Name Generator

This web application helps you brainstorm a catchy name for your new company. It uses a stepped process to guide you from your initial idea to a curated list of potential names, complete with domain availability checks.

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Setup Instructions

1.  **Clone the repository or download the files.**

2.  **Install dependencies:**
    Open your terminal or command prompt, navigate to the project directory, and run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure your Gemini API Key:**
    - Open the `config.py` file.
    - Replace `"YOUR_GEMINI_API_KEY"` with your actual Gemini API key. It is highly recommended to use an environment variable for this in a production environment.

## Running the Application

1.  **Start the Backend Server:**
    In your terminal, from the project directory, run:
    ```bash
    python app.py
    ```
    This will start the Flask backend server on `http://127.0.0.1:5001`. You should see output indicating that the server is running.

2.  **Open the Frontend:**
    - Navigate to the project directory in your file explorer.
    - Open the `index.html` file in your web browser (e.g., by double-clicking it).

## How to Use

1.  **Step 1: Define Your Idea**
    - Fill in the initial form with your company's headline, a description of what it does, who it's for, and its key features.
    - Click "Get UVP".

2.  **Step 2: Validate Your UVP**
    - The application will display an AI-generated Unique Value Proposition (UVP).
    - You can edit the UVP in the text area to better fit your vision.
    - Click "Next: Generate Lexicon".

3.  **Step 3: Curate Your Lexicon**
    - A list of AI-generated words and concepts will be displayed.
    - Uncheck any words that you don't think are relevant to your brand.
    - Click "Next: Generate Names".

4.  **Step 4: Choose Your Name**
    - The final list of AI-generated company names will be displayed.
    - Each name includes its `.com` domain availability and a list of potential competitors.
