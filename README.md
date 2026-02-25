# ATS Resume Analyzer - Simple Guide

## What is this app?

This is a web application that helps you check if your resume is good enough for management jobs. It acts like a robot recruiter (called ATS - Applicant Tracking System) and tells you:

- How well your resume matches the job you want
- What's good about your resume
- What needs improvement

## Supported Job Roles

You can check your resume for these 5 management positions:

1. **Product Manager** - Leads product development
2. **Project Manager** - Manages projects and teams
3. **Business Analyst** - Analyzes business needs
4. **Operations Manager** - Manages daily operations
5. **HR Manager** - Manages human resources

---

## How to Use This App

### Option 1: Upload a File

1. Drag and drop your resume file onto the upload area
2. Or click to browse and select your file
3. Supported files: PDF, DOCX, PNG, JPG, WebP (images get text extracted using OCR)
4. Select the job role you're targeting from the dropdown
5. Click "Analyze [filename]" button
6. Wait for the analysis to complete

### Option 2: Paste Resume Text

1. Select the job role from the dropdown
2. Click "Load Sample Resume" to see an example (optional)
3. Paste your resume text in the text box
4. Click "Analyze Resume" button

---

## Understanding Your Results

### Overall Score (0-100)

| Score | Meaning | Color |
|-------|---------|-------|
| 70-100 | High chance of getting shortlisted | Green |
| 50-69 | Medium chance | Orange |
| Below 50 | Low chance | Red |

### Score Breakdown

| Category | Max Points | What It Checks |
|----------|------------|----------------|
| Role Relevance | 30 | Does your resume have the right keywords for the job? |
| Leadership & Ownership | 25 | Do you show leadership and decision-making? |
| Impact & Metrics | 20 | Do you include numbers and results? (like "increased sales by 25%") |
| Resume Structure | 15 | Is your resume easy to read with clear sections? |
| Language Quality | 10 | Do you use strong action words? |

### Strengths
What you're doing right - these are the good parts of your resume.

### Weaknesses
What needs improvement - issues that might hurt your chances.

### Improvement Suggestions
Specific advice on how to improve your resume for your target role.

---

## How the App Works (Simple Explanation)

### Frontend (What You See)
- Built with React (a JavaScript framework)
- Handles file uploads and displays results
- Dark/Light theme support
- File preview for PDFs and images

### Backend (The Brain)
- Built with Python FastAPI
- Does all the resume analysis
- Extracts text from PDF, Word, and image files

### Analysis Process

1. **Text Extraction**: If you upload a file, the system extracts the text from it
2. **Keyword Matching**: Checks if your resume contains relevant words for your target role
3. **Leadership Check**: Looks for words like "led", "managed", "spearheaded"
4. **Metrics Check**: Finds numbers, percentages, and dollar amounts
5. **Structure Check**: Looks for clear sections and bullet points
6. **Language Check**: Counts action verbs and outcome words

---

## Running the App

### Using Docker (Easiest)

```bash
# Make sure Docker is installed
# Run this command in the project folder:
docker-compose up
```

- Frontend opens at: http://localhost:5173
- Backend API at: http://localhost:8000

### Running Separately

**Backend:**
```bash
cd backkend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## Project Structure

```
ResumeAnalyzer/
├── backkend/               # Python backend
│   └── app/
│       ├── main.py         # App setup
│       ├── api/            # API routes
│       │   └── resume.py   # Resume upload & analyze endpoints
│       └── services/       # Business logic
│           └── ats_engine.py  # Core analysis engine
│
├── frontend/               # React frontend
│   └── src/
│       ├── App.tsx         # Main app component
│       ├── components/     # UI pieces
│       │   ├── ScoreCard.tsx
│       │   ├── ResultsPanel.tsx
│       │   ├── PDFViewer.tsx
│       │   └── ImageViewer.tsx
│       ├── services/       # API calls
│       │   └── api.ts
│       └── types/          # Type definitions
│           └── ats.ts
│
├── docker-compose.yml      # Docker setup
├── README.md               # This file
```

---

## Key Files Explained

### Backend Files

- **`main.py`**: Sets up the web server and connects all parts
- **`resume.py`**: Handles file uploads and API endpoints
- **`ats_engine.py`**: The main brain - analyzes resumes and calculates scores

### Frontend Files

- **`App.tsx`**: The main page with upload form and results display
- **`api.ts`**: Sends requests to the backend
- **`ScoreCard.tsx`**: Shows individual score categories
- **`ResultsPanel.tsx`**: Shows strengths, weaknesses, suggestions
- **`sampleResumes.ts`**: Example resumes for each job role

---

## Technology Stack

| Part | Technology |
|------|------------|
| Frontend Framework | React + TypeScript |
| Build Tool | Vite |
| Backend Framework | FastAPI (Python) |
| PDF Processing | PyPDF2 |
| Word Processing | python-docx |
| Image OCR | Tesseract |
| Web Server | Nginx (production) |

---

## Troubleshooting

**File won't upload?**
- Make sure it's PDF, DOCX, PNG, JPG, or WebP format

"No text extracted" error?
- Your file might be an image scan - try a text-based PDF instead
- Or paste your resume text directly

Analysis taking too long?
- Image processing (OCR) takes time, especially for large files

---

## Want to Customize?

- **Add new job roles**: Edit `ats_engine.py` and add to `ROLE_KEYWORDS`
- **Change scoring weights**: Modify the max points in the evaluate function
- **Add more suggestions**: Update `_generate_suggestions` in ats_engine.py

---

## License

This is a learning/demo project.# ResumeAnalyzer
