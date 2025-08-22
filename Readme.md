
# CredTech

CredTech is a modern, full-stack platform for explainable company credit scoring. It combines a robust FastAPI backend with a sleek React + TypeScript frontend, providing interactive dashboards, financial insights, and news sentiment analysis.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [API Endpoints](#api-endpoints)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- **Company Selector:** Search and select companies to view their credit scores and financial details.
- **Dashboard:** Interactive dashboard showing credit score, trends, feature contributions, and news sentiment.
- **Score Card:** Elegant card component displaying the current credit score, breakdown, and explanations.
- **Feature Contributions:** Visualize how financial metrics and news impact the score.
- **News List:** Latest news articles with sentiment analysis.
- **Explainability:** Transparent scoring logic with detailed breakdowns.
- **Responsive Design:** Optimized for desktop and mobile.
- **API-first:** FastAPI backend with RESTful endpoints.

---

## Tech Stack

**Frontend**
- React (TypeScript)
- Vite
- Tailwind CSS
- Bun (or npm/yarn)
- Lucide Icons

**Backend**
- FastAPI (Python)
- Supabase (PostgreSQL, authentication, storage)
- Machine Learning (scikit-learn, joblib)
- Docker

---

## Project Structure

```
CredTech-Vercel/
├── Backend/
│   ├── app/
│   │   ├── api/           # API route modules
│   │   ├── data/          # Data scripts and ML models
│   │   ├── ml/            # Scoring and explainability logic
│   │   ├── models/        # Data models
│   │   ├── utils/         # Utility functions (DB, etc.)
│   │   ├── main.py        # FastAPI entrypoint
│   │   └── config.py      # Configuration
│   ├── requirements.txt   # Python dependencies
│   ├── Dockerfile         # Container setup
│   └── README.md          # Backend documentation
├── Frontend/
│   ├── public/            # Static assets
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── lib/           # Utility functions
│   │   ├── pages/         # Page components
│   │   ├── services/      # API service layer
│   │   ├── assets/        # Images and SVGs
│   │   └── App.tsx        # Main app component
│   ├── package.json       # Project metadata and scripts
│   ├── tailwind.config.ts # Tailwind CSS configuration
│   ├── vite.config.ts     # Vite configuration
│   └── README.md          # Frontend documentation
```

---

## Getting Started

### Backend

#### Prerequisites
- Python 3.10+
- Supabase account & project (or PostgreSQL DB)
- Docker (optional)

#### Setup

1. **Clone the repository**
	```sh
	git clone <YOUR_GIT_URL>
	cd CredTech-Vercel/Backend
	```

2. **Create and activate a virtual environment**
	```sh
	python -m venv myenv
	.\\myenv\\Scripts\\activate
	```

3. **Install dependencies**
	```sh
	pip install -r requirements.txt
	```

4. **Configure environment variables**
	- Copy `.env.example` to `.env` and fill in your Supabase credentials.

5. **Run the backend server**
	```sh
	uvicorn app.main:app --reload
	```

6. **(Optional) Run with Docker**
	```sh
	docker build -t credtech-backend .
	docker run -p 8000:8000 credtech-backend
	```

### Frontend

#### Prerequisites
- Node.js (v18+ recommended)
- Bun (or npm/yarn)

#### Setup

1. **Navigate to the frontend directory**
	```sh
	cd CredTech-Vercel/Frontend
	```

2. **Install dependencies**
	```sh
	bun install
	# or
	npm install
	```

3. **Run the development server**
	```sh
	bun run dev
	# or
	npm run dev
	```

4. **Open the app**
	- Visit `http://localhost:5173` in your browser.

---

## API Endpoints

**Base URL:** `http://localhost:8000`

- `GET /companies` — List all companies
- `GET /company/{ticker}` — Get details for a company
- `GET /news/{ticker}` — Get recent news for a company
- `GET /score/{ticker}` — Get credit score and explainability breakdown
- `GET /score_history/{ticker}` — Get historical scores

---

## Customization

- **Frontend Theme:** Edit `tailwind.config.ts` for colors and styles.
- **Backend Logic:** Modify scoring and explainability in `app/ml/`.
- **API Contracts:** Update models in `app/models/` and `src/hooks/api.ts`.

---

## Contributing

We welcome contributions! Please fork the repository, create a feature branch, and submit a pull request. Follow the code style and include clear commit messages.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- [React](https://react.dev/)
- [Vite](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Supabase](https://supabase.com/)
- [Bun](https://bun.sh/)
- [Lucide Icons](https://lucide.dev/)

---

> Crafted with care by the CredTech team. For questions or support, please open an issue or contact us directly.
