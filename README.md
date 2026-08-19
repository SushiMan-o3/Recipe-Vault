# Recipe Vault

Recipe Vault is a recipe manager that lets you save recipes three ways — paste a URL, upload a photo/PDF of a recipe, or type one in by hand — and uses Claude to turn messy scraped or scanned text into clean, structured recipe data automatically.

## Inspiration
My brother loves cooking and so do I. I thought it would be a good idea for me to store all of the recipes that me and my family would enjoy cooking and store it for future use. 

I decided to make this project in order to learn CRUD, Full Stack Development and RESTapis. 

## Features

- **Add a recipe from a URL** — scrapes the page and lets Claude extract the recipe from the raw text.
- **Add a recipe from a file** — upload an image, PDF, or text file (e.g. a photo of a handwritten recipe card) and Claude extracts the text and structures it.
- **Manual entry** — skip AI entirely and fill out the recipe form yourself.
- **Review before saving** — every AI-parsed recipe is shown back to you for editing/confirmation before it's written to the database.
- **Browse & search** — paginated recipe list with search across title, description, and notes.
- **Auto-assigned emoji** — each recipe gets an emoji based on keyword matching against its title/description/ingredients.
- Full CRUD on recipes (create, read, update, delete), with ingredients and equipment stored per recipe.

## How it works

There are three entry points for adding a recipe, and they converge before hitting the database:

1. **URL input** → backend scrapes the page (`httpx` + `BeautifulSoup`) → raw text handed to Claude.
2. **File upload** → Claude reads the image/PDF/text directly (vision/document input) and returns markdown text.
3. **Manual entry** → skips AI entirely; the user fills out a form.

For the URL and file paths, the extracted text is sent to Claude along with a structured prompt (`api/config.py`) that instructs it to return recipe/ingredients/equipment as strict JSON matching the database schema. The result is shown to the user on a review screen where they can edit anything before it's saved. All three paths end at the same `POST /recipe_to_db` call.

## Tech stack

**Frontend**
- React 19 + Vite
- React Router for navigation
- Axios for API calls (`src/api/api.js`)

**Backend**
- FastAPI (Python)
- Pydantic for request/response schemas
- `psycopg2` for direct SQL against Postgres
- `httpx` + `BeautifulSoup4` for scraping recipe URLs
- Deployed as a Vercel serverless function (`vercel.json` rewrites all routes to `api/app`)

**Database**
- [Neon](https://neon.tech) — serverless Postgres, connected via `DATABASE_URL`

**AI**
- Anthropic Claude API (`claude-haiku-4-5`) for:
  - extracting text from uploaded images/PDFs
  - parsing scraped/extracted text into structured recipe JSON

## Project structure

```
Recipe-Vault/
├── backend/
│   ├── api/
│   │   ├── app.py        # FastAPI app: routes, schemas, Claude + scraping logic
│   │   ├── database.py   # Postgres connection + table setup
│   │   └── config.py     # Claude parsing prompt
│   ├── main.py            # local dev entrypoint (uvicorn)
│   └── vercel.json        # serverless deployment config
└── frontend/
    └── src/
        ├── api/api.js      # Axios wrapper for all backend calls
        ├── pages/          # Landing, Home, AddRecipe, ReviewRecipe, RecipeDetail
        └── components/     # Navbar, RecipeCard, SearchBar
```

## Getting started

### Prerequisites

- Python 3.11+
- Node.js 18+
- A Postgres database (e.g. a free [Neon](https://neon.tech) project)
- An [Anthropic API key](https://console.anthropic.com/)

### Backend

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in `backend/`:

```
CLAUDE_TOKEN=your_anthropic_api_key
DATABASE_URL=your_postgres_connection_string
FRONTEND_URL=http://localhost:5173
```

Run the API:

```bash
python main.py
```

The server starts on `http://127.0.0.1:8000` and creates the required tables (`recipes`, `ingredients`, `equipments`) on first run.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs on `http://localhost:5173`. Optionally set `VITE_API_URL` in a `.env` file to point at a non-default backend URL.

## API reference

| Method | Endpoint               | Description                                      |
| ------ | ----------------------- | ------------------------------------------------- |
| GET    | `/recipes`              | List recipes (supports `query`, `page`, `limit`) |
| GET    | `/{recipeid}`           | Get a single recipe                              |
| POST   | `/url_to_json`          | Scrape a URL and parse it into recipe JSON        |
| POST   | `/upload_file_to_json`  | Extract + parse a recipe from an uploaded file    |
| POST   | `/recipe_to_db`         | Save a (reviewed) recipe to the database          |
| PUT    | `/{recipeid}`           | Update an existing recipe                         |
| DELETE | `/{recipeid}`           | Delete a recipe                                   |

## Deployment

The backend is set up to deploy to Vercel as a serverless function — `vercel.json` rewrites all incoming routes to `api/app`. The frontend can be deployed independently (e.g. also on Vercel) with `VITE_API_URL` pointed at the deployed backend.
