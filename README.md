# Project Name

This project consists of a Vite-based frontend client and a FastAPI backend server.

## Prerequisites

- [Node.js](https://nodejs.org/)
- [pnpm](https://pnpm.io/)
- [Python](https://www.python.org/) (3.8 or higher)
- [Poetry](https://python-poetry.org/)

## Setup Instructions

### Frontend Setup (Client)

1. Navigate to the client directory:

```bash
cd client
```

2. Install dependencies:

```bash
pnpm install
```

3. Start the development server:

```bash
pnpm run dev
```

The frontend development server should now be running and accessible at `http://localhost:5173`

### Backend Setup (Server)

1. Navigate to the server directory:

```bash
cd server
```

2. Install Python dependencies using Poetry:

```bash
poetry install
```

3. Install Playwright:

```bash
poetry run playwright install
```

4. Start the FastAPI server:

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8090
```

The backend server will be running at `http://localhost:8090`

## Development

- Frontend development server runs on port 5173 by default
- Backend API server runs on port 8090
- API documentation is available at `http://localhost:8090/docs`

## License

[Add your license information here]
