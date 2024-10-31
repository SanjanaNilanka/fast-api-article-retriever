# Random News API

This FastAPI application provides an endpoint to fetch random news articles from various sources.

## Endpoints

### GET /api/random-article

Returns a random article with the following information:
- Title
- Full text
- Summary
- Authors
- URL
- Source URL
- Publish date (if available)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

The API will be available at http://localhost:8000

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc