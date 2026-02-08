# 🔗 **HR-Agent - RAG-Based Intelligent Resume Screening**

<div align="center">

![AI HR Agent](https://img.shields.io/badge/AI-HR%20Agent-purple?style=for-the-badge&logo=robot)
![FastAPI](https://img.shields.io/badge/FastAPI-Python-green?style=for-the-badge&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)
![GPT-4](https://img.shields.io/badge/OpenAI-GPT--4-blue?style=for-the-badge&logo=openai)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-purple?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/Neon-PostgreSQL-blue?style=for-the-badge&logo=postgresql)

### **AI-Powered Resume Screening with Retrieval Augmented Generation**

*Upload 100 resumes, get the top 5 candidates using semantic search and GPT-4 evaluation*

[Live Demo](#) · [Report Bug](#) · [Request Feature](#)

</div>

---

## 🎯 **Overview**

**HR-Agent** is an intelligent recruitment automation system that uses RAG (Retrieval Augmented Generation) to evaluate job applicants at scale. By combining vector embeddings for semantic search with GPT-4's advanced reasoning, HR-Agent identifies the most qualified candidates from large applicant pools in minutes, not days.

Built for HR professionals, recruiters, and hiring managers who need to process hundreds of resumes efficiently while maintaining high-quality candidate evaluation.

---

## ✨ **Key Features**

### 🔍 **Intelligent Resume Processing**
- **Bulk Upload** - Process up to 100+ resumes simultaneously
- **PDF Parsing** - Automatic text extraction from PDF resumes
- **Semantic Understanding** - AI comprehends context, not just keywords
- **Fast Processing** - Complete evaluation in under 2 minutes

### 🧠 **RAG-Powered Evaluation**
- **Vector Embeddings** - Transform resumes into semantic representations
- **Similarity Search** - Pinecone finds the most relevant candidates
- **GPT-4 Analysis** - Deep evaluation of top candidates
- **Multi-Dimensional Scoring** - Rate candidates across multiple criteria

### 📊 **Comprehensive Insights**
- **Top 5 Rankings** - Clear winner identification with confidence scores
- **Detailed Analysis** - Strengths, weaknesses, and fit assessment
- **Comparison View** - Side-by-side candidate comparison
- **Export Reports** - Download evaluation results as PDF

### 💼 **Professional Interface**
- **Modern Dashboard** - Clean, intuitive UI built with Next.js
- **Real-Time Progress** - Live updates during evaluation
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark Mode** - Eye-friendly interface for extended use

---

## 🏗️ **Architecture**

### **RAG Pipeline Flow**

```mermaid
graph LR
    A[100 Resumes] --> B[PDF Parser]
    B --> C[Text Extraction]
    C --> D[OpenAI Embeddings]
    D --> E[Pinecone Vector DB]
    E --> F[Top 15 Retrieval]
    F --> G[GPT-4 Evaluation]
    G --> H[Top 5 Ranked Results]
    H --> I[PostgreSQL Storage]
```

### **How It Works**

1. **Upload Phase**
   - HR uploads job description and candidate resumes (PDF format)
   - System extracts text content from all PDFs
   - Validates and stores resume data

2. **Embedding Phase**
   - Each resume is converted to a 1536-dimensional vector using OpenAI's text-embedding-3-small
   - Vectors capture semantic meaning, not just keywords
   - Embeddings stored in Pinecone for fast retrieval

3. **Retrieval Phase**
   - Job description is also embedded
   - Pinecone performs cosine similarity search
   - Top 15 most semantically similar resumes retrieved

4. **Evaluation Phase**
   - GPT-4 analyzes each of the 15 candidates in detail
   - Evaluates across multiple dimensions (skills, experience, culture fit)
   - Scores candidates on 0-100 scale with detailed reasoning

5. **Ranking Phase**
   - Top 5 candidates selected based on GPT-4 scores
   - Results stored in PostgreSQL for future reference
   - Detailed reports generated with recommendations

---

## 🛠️ **Tech Stack**

<div align="center">

| Category | Technologies |
|----------|-------------|
| **Backend** | FastAPI (Python), OpenAI API (GPT-4 + Embeddings), Pinecone, SQLAlchemy |
| **Frontend** | Next.js 14, TypeScript, React, Tailwind CSS, shadcn/ui |
| **Database** | Neon PostgreSQL (Serverless), Pinecone (Vector DB) |
| **Infrastructure** | Docker, Docker Compose, Vercel (Frontend), Render/Railway (Backend) |
| **ML/AI** | OpenAI GPT-4, OpenAI Embeddings (text-embedding-3-small) |

</div>

---

## 🚀 **Getting Started**

### **Prerequisites**

- Python 3.9+ (for backend)
- Node.js 18+ (for frontend)
- OpenAI API key with GPT-4 access
- Pinecone API key (free tier available)
- Neon PostgreSQL database (or any PostgreSQL instance)

### **Installation**

#### **1. Clone the Repository**

```bash
git clone https://github.com/sharathkum05/HR-Agent.git
cd HR-Agent
```

#### **2. Backend Setup**

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Set up environment variables:**

Create `.env` file in the `backend/` directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=us-east-1-aws
PINECONE_INDEX_NAME=hr-agent-resumes

# Database Configuration
DATABASE_URL=postgresql://user:password@host:5432/hr_agent

# Application Configuration
ENVIRONMENT=development
DEBUG=True
MAX_RESUMES_PER_JOB=100
```

**Initialize the database:**

```bash
# Run migrations
alembic upgrade head

# Or create tables directly
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

**Start the backend server:**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

API documentation at: `http://localhost:8000/docs`

#### **3. Frontend Setup**

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
# or
yarn install
# or
pnpm install
```

**Set up environment variables:**

Create `.env.local` file in the `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=HR Agent
```

**Start the development server:**

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Frontend will be available at: `http://localhost:3000`

#### **4. Docker Setup (Alternative)**

For a containerized setup:

```bash
# From project root
docker-compose up --build

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## 📖 **Usage Guide**

### **Step 1: Create a Job Posting**

1. Navigate to the dashboard
2. Click "Create New Job"
3. Enter job details:
   - **Job Title** (e.g., "Senior Software Engineer")
   - **Job Description** (detailed requirements, skills, experience)
   - **Department** (optional)
   - **Location** (optional)

### **Step 2: Upload Resumes**

1. Click "Upload Resumes" for your job posting
2. Select up to 100 PDF files
3. System will:
   - Validate file format
   - Extract text content
   - Display upload progress
   - Confirm successful uploads

### **Step 3: Run Evaluation**

1. Click "Run Evaluation" button
2. Watch real-time progress:
   - ✅ Generating embeddings... (15-30s)
   - ✅ Searching vector database... (2-5s)
   - ✅ Evaluating top candidates with GPT-4... (60-90s)
   - ✅ Ranking results... (1-2s)

### **Step 4: Review Results**

View the top 5 candidates with:
- **Overall Score** (0-100)
- **Skill Match** - How well skills align with requirements
- **Experience Level** - Years and relevance of experience
- **Education** - Academic qualifications
- **Culture Fit** - Soft skills and values alignment
- **Key Highlights** - Standout achievements
- **Potential Concerns** - Areas needing clarification

### **Step 5: Export & Take Action**

- Download detailed report as PDF
- Share results with hiring team
- Schedule interviews with top candidates
- Archive job posting for future reference



## 🏗️ **Project Structure**

```
HR-Agent/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py            # FastAPI application entry
│   │   ├── config.py          # Configuration settings
│   │   ├── database.py        # Database connection
│   │   ├── models/            # SQLAlchemy models
│   │   │   ├── job.py
│   │   │   ├── resume.py
│   │   │   └── evaluation.py
│   │   ├── services/          # Business logic
│   │   │   ├── pdf_parser.py
│   │   │   ├── embedding_service.py
│   │   │   ├── pinecone_service.py
│   │   │   └── evaluation_service.py
│   │   ├── api/               # API routes
│   │   │   ├── jobs.py
│   │   │   ├── resumes.py
│   │   │   └── evaluations.py
│   │   └── schemas/           # Pydantic schemas
│   ├── alembic/               # Database migrations
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile
├── frontend/                   # Next.js Frontend
│   ├── src/
│   │   ├── app/               # Next.js 14 App Router
│   │   │   ├── page.tsx       # Home page
│   │   │   ├── jobs/          # Job management pages
│   │   │   └── api/           # API routes (if needed)
│   │   ├── components/        # React components
│   │   │   ├── ui/            # shadcn/ui components
│   │   │   ├── JobCard.tsx
│   │   │   ├── ResumeUploader.tsx
│   │   │   ├── EvaluationProgress.tsx
│   │   │   └── CandidateRanking.tsx
│   │   ├── lib/               # Utilities
│   │   │   ├── api.ts         # API client
│   │   │   └── utils.ts
│   │   └── types/             # TypeScript types
│   ├── public/                # Static assets
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml         # Docker orchestration
├── ARCHITECTURE_PLAN.md       # Detailed architecture
├── IMPLEMENTATION_GUIDE.md    # Implementation steps
└── README.md                  # This file
```

---

## 🔧 **API Reference**

### **Base URL**
```
http://localhost:8000/api/v1
```

### **Endpoints**

#### **Jobs**

**Create Job**
```http
POST /jobs
Content-Type: application/json

{
  "title": "Senior Software Engineer",
  "description": "We are looking for...",
  "department": "Engineering",
  "location": "San Francisco, CA"
}

Response: 201 Created
{
  "id": "job_123",
  "title": "Senior Software Engineer",
  "status": "active",
  "created_at": "2026-02-08T08:00:00Z"
}
```

**Get Job Details**
```http
GET /jobs/{job_id}

Response: 200 OK
{
  "id": "job_123",
  "title": "Senior Software Engineer",
  "description": "...",
  "total_resumes": 47,
  "evaluation_status": "completed"
}
```

#### **Resumes**

**Upload Resumes (Bulk)**
```http
POST /jobs/{job_id}/resumes
Content-Type: multipart/form-data

files: [resume1.pdf, resume2.pdf, ...]

Response: 200 OK
{
  "job_id": "job_123",
  "uploaded_count": 47,
  "failed_count": 0,
  "resume_ids": ["res_1", "res_2", ...]
}
```

**Get Resume Details**
```http
GET /resumes/{resume_id}

Response: 200 OK
{
  "id": "res_1",
  "filename": "john_doe_resume.pdf",
  "text_content": "...",
  "upload_date": "2026-02-08T08:05:00Z"
}
```

#### **Evaluations**

**Trigger Evaluation**
```http
POST /jobs/{job_id}/evaluate

Response: 202 Accepted
{
  "job_id": "job_123",
  "status": "processing",
  "estimated_time": "90 seconds"
}
```

**Get Evaluation Status**
```http
GET /jobs/{job_id}/evaluation-status

Response: 200 OK
{
  "status": "completed",
  "progress": 100,
  "current_step": "ranking_results",
  "top_candidates_count": 5
}
```

**Get Top Candidates**
```http
GET /jobs/{job_id}/top-candidates

Response: 200 OK
{
  "job_id": "job_123",
  "candidates": [
    {
      "rank": 1,
      "resume_id": "res_42",
      "candidate_name": "John Doe",
      "overall_score": 94,
      "scores": {
        "technical_skills": 95,
        "experience": 92,
        "education": 88,
        "culture_fit": 96
      },
      "highlights": [
        "10+ years of Python experience",
        "Led team of 15 engineers",
        "MS in Computer Science from Stanford"
      ],
      "concerns": [
        "Limited cloud infrastructure experience"
      ],
      "recommendation": "Strong hire"
    }
    // ... 4 more candidates
  ]
}
```

---

## 💰 **Cost Estimation**

### **Per 100 Resumes Evaluation**

| Component | Usage | Cost |
|-----------|-------|------|
| **Embeddings** | 100 resumes × ~1000 tokens | $0.05 |
| **Vector Search** | Pinecone query | $0.00 (free tier) |
| **GPT-4 Analysis** | 15 candidates × ~4000 tokens | $1.50 |
| **Database** | Neon PostgreSQL storage | $0.00 (free tier) |
| **Total** | | **~$1.55 per batch** |

### **Monthly Cost Estimates**

**Small HR Team (10 jobs/month, 50 resumes each)**
- Embeddings: $2.50
- GPT-4 Evaluations: $7.50
- **Total: ~$10/month**

**Medium Recruiting Firm (50 jobs/month, 100 resumes each)**
- Embeddings: $25
- GPT-4 Evaluations: $75
- **Total: ~$100/month**

**Large Enterprise (200 jobs/month, 100 resumes each)**
- Embeddings: $100
- GPT-4 Evaluations: $300
- Pinecone: $70 (paid tier)
- **Total: ~$470/month**



## 🧪 **Development**

### **Available Scripts**

**Backend:**
```bash
# Start development server
uvicorn app.main:app --reload

# Run tests
pytest

# Format code
black app/
isort app/

# Type checking
mypy app/

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

**Frontend:**
```bash
# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm run start

# Run linter
npm run lint

# Type check
npm run type-check
```

### **Environment Variables**

**Backend (.env):**
```env
# Required
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
DATABASE_URL=postgresql://...

# Optional
PINECONE_ENVIRONMENT=us-east-1-aws
PINECONE_INDEX_NAME=hr-agent-resumes
MAX_RESUMES_PER_JOB=100
EMBEDDING_MODEL=text-embedding-3-small
EVALUATION_MODEL=gpt-4-turbo-preview
TOP_K_RETRIEVAL=15
FINAL_CANDIDATES=5
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=HR Agent
NEXT_PUBLIC_MAX_FILE_SIZE=5242880
```

---

## 🚀 **Deployment**

### **Backend Deployment (Render/Railway)**

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Render**
   - Create new Web Service
   - Connect GitHub repository
   - Set build command: `pip install -r backend/requirements.txt`
   - Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables

3. **Configure Database**
   - Create Neon PostgreSQL instance
   - Copy connection string to `DATABASE_URL`

4. **Set up Pinecone**
   - Create index: `hr-agent-resumes`
   - Dimension: 1536
   - Metric: cosine
   - Copy API key to environment

### **Frontend Deployment (Vercel)**

1. **Import to Vercel**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import GitHub repository
   - Root directory: `frontend`

2. **Configure**
   - Framework: Next.js
   - Build command: `npm run build`
   - Output directory: `.next`

3. **Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
   ```

4. **Deploy**
   - Click "Deploy"
   - Access at: `https://your-project.vercel.app`



## 🤝 **Contributing**

Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### **Contribution Guidelines**

- Follow PEP 8 for Python code
- Use TypeScript for all frontend code
- Write tests for new features
- Update documentation
- Keep commits atomic and well-described

---

## 📄 **License**

Distributed under the MIT License. See `LICENSE` file for more information.

---

## 👨‍💻 **Author**

**Sharath Kumar**
- GitHub: [@sharathkum05](https://github.com/sharathkum05)
- LinkedIn: [Sharath Kumar](https://linkedin.com/in/sharathkum05)

---

## 🙏 **Acknowledgments**

- **OpenAI** - For GPT-4 and embedding models that power intelligent evaluation
- **Pinecone** - For lightning-fast vector similarity search
- **FastAPI** - For the high-performance Python backend framework
- **Next.js** - For the incredible React framework and developer experience
- **shadcn/ui** - For beautiful, accessible UI components
- **Neon** - For serverless PostgreSQL hosting
- **Vercel** - For seamless frontend deployment

---

## 📚 **Additional Resources**

- [Architecture Plan](./ARCHITECTURE_PLAN.md) - Detailed system design
- [Implementation Guide](./IMPLEMENTATION_GUIDE.md) - Step-by-step development guide
- [API Documentation](http://localhost:8000/docs) - Interactive API docs (when running)
- [RAG Best Practices](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)



<div align="center">

**Built with 💜 by Sharath Kumar**

*Transforming recruitment with AI, one resume at a time*

If HR-Agent helps streamline your hiring, please consider giving it a ⭐️

[⬆ Back to Top](#--hr-agent---rag-based-intelligent-resume-screening)

</div>
