# Math Notes Calculator Backend

This is the backend for the Math Notes Calculator application, built with FastAPI and using Google's Gemini AI for image analysis.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/math-notes-calculator-backend.git
   cd math-notes-calculator-backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     .\venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the root directory and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Running the Application

To start the FastAPI server:

```
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`.

## API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
math-notes-calculator-backend/
│
├── apps/
│   └── calculator/
│       ├── __init__.py
│       ├── route.py
│       └── utils.py
│
├── venv/
├── .env
├── .gitignore
├── constants.py
├── main.py
├── README.md
└── requirements.txt
```

## Key Components

- `main.py`: The entry point of the application. It sets up the FastAPI app and includes the router for the calculator.
- `apps/calculator/route.py`: Contains the API endpoints for the calculator functionality.
- `apps/calculator/utils.py`: Includes utility functions for image analysis and mathematical operations.
- `constants.py`: Stores constant values and configurations.

## Environment Variables

Make sure to set the following environment variables in your `.env` file:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Dependencies

The main dependencies for this project are:

- FastAPI
- Uvicorn
- Google Generative AI
- Pillow
- python-dotenv

For a complete list of dependencies, see the `requirements.txt` file:

```
annotated-types==0.7.0
anyio==4.4.0
cachetools==5.5.0
certifi==2024.8.30
charset-normalizer==3.3.2
click==8.1.7
fastapi==0.112.2
google-ai-generativelanguage==0.6.6
google-api-core==2.19.2
google-api-python-client==2.143.0
google-auth==2.34.0
google-auth-httplib2==0.2.0
google-generativeai==0.7.2
googleapis-common-protos==1.65.0
grpcio==1.66.1
grpcio-status==1.62.3
h11==0.14.0
httplib2==0.22.0
idna==3.8
pillow==10.4.0
proto-plus==1.24.0
protobuf==4.25.4
pyasn1==0.6.0
pyasn1_modules==0.4.0
pydantic==2.8.2
pydantic_core==2.20.1
pyparsing==3.1.4
python-dotenv==1.0.1
requests==2.32.3
rsa==4.9
sniffio==1.3.1
starlette==0.38.2
tqdm==4.66.5
typing_extensions==4.12.2
uritemplate==4.1.1
urllib3==2.2.2
uvicorn==0.30.6
```

## Troubleshooting

If you encounter issues with the Gemini API key:

1. Ensure the `GEMINI_API_KEY` is correctly set in your `.env` file.
2. If using Windows, you can set the environment variable temporarily in your current command prompt session:
   ```
   set GOOGLE_API_KEY=your_actual_api_key_here
   ```
3. Alternatively, configure the API key in your Python code:
   ```python
   import google.generativeai as genai
   
   genai.configure(api_key='your_actual_api_key_here')
   ```
4. Verify that your Gemini API key is valid and has the necessary permissions.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
