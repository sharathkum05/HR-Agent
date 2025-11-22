# HR Agent - RAG-Based Intelligent Resume Screening

An AI-powered HR agent that uses RAG (Retrieval Augmented Generation) to intelligently evaluate job applicants. Upload 100 resumes and get the top 5 candidates using semantic search and GPT-4 evaluation.

## Features

- **RAG Pipeline**: Vector embeddings for retrieval + GPT-4 for generation
- **Pinecone Integration**: Fast vector similarity search
- **Neon PostgreSQL**: Serverless database for persistence
- **Modern UI**: Next.js, TypeScript, React with Tailwind CSS
- **Bulk Processing**: Handle 100+ resumes efficiently
- **Intelligent Scoring**: Multi-dimensional candidate evaluation

## Architecture

```
100 Resumes → Embeddings → Pinecone → Top 15 Retrieval → GPT-4 Evaluation → Top 5 Results
```

## Tech Stack

### Backend
- FastAPI (Python)
- OpenAI API (GPT-4 + embeddings)
- Pinecone (Vector database)
- Neon PostgreSQL (Database)
- SQLAlchemy (ORM)

### Frontend
- Next.js 14 (App Router)
- TypeScript
- React
- Tailwind CSS
- shadcn/ui components

## Setup

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys:
# - OPENAI_API_KEY
# - PINECONE_API_KEY
# - DATABASE_URL (Neon PostgreSQL)
```

5. Initialize database:
```bash
alembic upgrade head
```

6. Run backend:
```bash
uvicorn app.main:app --reload
```

Backend will run on http://localhost:8000

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Run frontend:
```bash
npm run dev
```

Frontend will run on http://localhost:3000

## Usage

1. **Create Job**: Enter job title and description
2. **Upload Resumes**: Upload up to 100 PDF resumes
3. **Run Evaluation**: Click "Run Evaluation" to start RAG pipeline
4. **View Results**: See top 5 candidates with detailed scores and analysis

## API Endpoints

- `POST /api/jobs` - Create job posting
- `GET /api/jobs/{id}` - Get job details
- `POST /api/jobs/{id}/resumes` - Upload resumes (bulk)
- `POST /api/jobs/{id}/evaluate` - Trigger evaluation
- `GET /api/jobs/{id}/top-candidates` - Get top 5 candidates

## Cost Estimation

Per 100 resumes:
- Embeddings: ~$0.05
- GPT-4 evaluations (15 candidates): ~$1.50
- **Total: ~$1.55 per batch**

## Project Structure

```
HR_Agent/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── services/
│   │   └── api/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   └── lib/
│   └── package.json
└── README.md
```

## Development

See detailed documentation:
- [ARCHITECTURE_PLAN.md](./ARCHITECTURE_PLAN.md)
- [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)

## License

MIT
