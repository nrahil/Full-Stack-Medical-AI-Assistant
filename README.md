# 🩺 Full-Stack Medical AI Assistant

[![CI Pipeline](https://github.com/nrahil/Full-Stack-Medical-AI-Assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/nrahil/Full-Stack-Medical-AI-Assistant/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Next.js 16](https://img.shields.io/badge/Next.js-16-black.svg?logo=next.js&logoColor=white)](https://nextjs.org/)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](docker-compose.yml)

> An intelligent, full-stack Medical AI Assistant that combines **Retrieval-Augmented Generation (RAG), Agentic AI, conversational memory, and secure authentication** to provide context-aware answers from user-uploaded medical documents.

Built with **Next.js, TypeScript, Python, LangChain, LangGraph, and modern vector search technologies**, this project demonstrates how Generative AI can be integrated into a production-style full-stack application.

---

## 🚀 Overview

The **Full-Stack Medical AI Assistant** allows users to upload medical documents such as PDF reports and interact with them through a conversational AI interface.

Instead of relying only on the LLM's pre-trained knowledge, the system uses **RAG** to retrieve relevant information from the user's documents before generating an answer.

The application also maintains **conversation history**, allowing users to ask follow-up questions while preserving the context of previous interactions.

The backend is designed around an **agentic workflow using LangGraph**, enabling intelligent routing and orchestration of different AI capabilities.

---

## ✨ Key Features

### 📄 Medical Document RAG

* Upload medical PDF documents.
* Automatically process and ingest documents.
* Split documents into meaningful chunks.
* Generate embeddings for semantic search.
* Retrieve the most relevant information for each question.
* Generate answers grounded in the uploaded documents.

### 🤖 Agentic AI Workflow

* Built using **LangGraph** for stateful AI workflows.
* Uses an agent-based architecture instead of a simple single LLM call.
* Dynamically determines how a user query should be processed.
* Supports extensible AI tools and workflow components.
* Maintains state throughout multi-step interactions.

### 🧠 Conversational Memory

* Maintains chat history across conversations.
* Stores conversation data using **SQLite**.
* Enables contextual follow-up questions.
* Allows the assistant to understand previous interactions instead of treating every query independently.

### 🔐 Authentication

* Secure user authentication using **Clerk**.
* User-specific access to the application.
* Separates user sessions and conversations.

### 💬 Full-Stack AI Chat Interface

* Modern responsive frontend built with **Next.js**.
* Real-time interaction with the AI backend.
* Clean conversational interface.
* Upload documents and immediately interact with them.

### 🔎 Context-Grounded Answers

The system follows a retrieval-based workflow:

```text
User Question
      ↓
Query Processing
      ↓
Retriever / Vector Search
      ↓
Relevant Medical Context
      ↓
LangGraph / Agentic Workflow
      ↓
LLM
      ↓
Context-Aware Response
```

This reduces the chance of generating answers unrelated to the user's uploaded documents.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │       User          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌────────────────────────────┐
                    │     Next.js Frontend      │
                    │   TypeScript + Tailwind   │
                    │          + Clerk           │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │      Python Backend        │
                    │        AI Engine           │
                    └─────────────┬──────────────┘
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
                 ▼                ▼                ▼
          ┌────────────┐   ┌─────────────┐  ┌─────────────┐
          │    RAG     │   │  LangGraph  │  │   Memory    │
          │  Pipeline  │   │   Agents    │  │   SQLite    │
          └─────┬──────┘   └──────┬──────┘  └─────────────┘
                │                 │
                ▼                 ▼
        ┌──────────────┐    ┌──────────────┐
        │ Vector Store │    │     LLM      │
        │  Embeddings  │    │  Generation  │
        └──────┬───────┘    └──────┬───────┘
               │                   │
               └─────────┬─────────┘
                         ▼
                  ┌──────────────┐
                  │ AI Response  │
                  └──────────────┘
```

---

# 🧠 RAG Pipeline

The document question-answering pipeline works in multiple stages:

### 1. Document Upload

The user uploads a medical PDF through the frontend.

### 2. Document Ingestion

The backend processes the document using the ingestion pipeline.

### 3. Chunking

The document is divided into smaller chunks so that relevant sections can be retrieved efficiently.

### 4. Embedding Generation

Each chunk is converted into a numerical vector representation.

### 5. Vector Storage

The embeddings are stored in a vector database for semantic retrieval.

### 6. Query Retrieval

When the user asks a question, the system searches for the most relevant document chunks.

### 7. Agentic Processing

The retrieved context is passed through the LangGraph workflow where the appropriate AI processing path is selected.

### 8. Response Generation

The LLM generates a response using the retrieved medical context and conversation history.

---

# 🤖 Agentic AI Workflow

Unlike a basic RAG chatbot where every question follows the same fixed pipeline, this project uses **LangGraph** to create a more flexible and stateful workflow.

```text
                  User Query
                      │
                      ▼
               ┌─────────────┐
               │   Agent /   │
               │   Router    │
               └──────┬──────┘
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
       Retrieve     Process     Other
       Documents    Context     Tools
          │           │           │
          └───────────┼───────────┘
                      ▼
                Final Response
```

This architecture makes the system easier to extend with additional tools and specialized agents.

---

# 🛠️ Tech Stack

## Frontend

* **Next.js**
* **TypeScript**
* **React**
* **Tailwind CSS**
* **Clerk Authentication**

## Backend

* **Python**
* **LangChain**
* **LangGraph**
* **RAG**
* **Vector Database**
* **SQLite**

## AI / Generative AI

* Large Language Models (LLMs)
* Embeddings
* Semantic Search
* Retrieval-Augmented Generation
* Agentic AI
* Stateful AI Workflows



---

# ⚙️ Getting Started

### Option A: Quickstart with Docker Compose (Recommended)

The easiest way to spin up both the FastAPI backend and Next.js frontend is using Docker Compose:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nrahil/Full-Stack-Medical-AI-Assistant.git
   cd Full-Stack-Medical-AI-Assistant
   ```

2. **Configure environment variables:**
   ```bash
   cp backend/.env.example backend/.env
   cp med-ai-frontend/.env.example med-ai-frontend/.env
   ```
   *Edit `backend/.env` with your Groq and Pinecone keys, and `med-ai-frontend/.env` with your Clerk keys.*

3. **Launch the services:**
   ```bash
   docker compose up --build
   ```
   * Backend will be accessible at: `http://localhost:8000`
   * Frontend will be accessible at: `http://localhost:3000`

---

### Option B: Manual Local Setup

#### 1. Backend Setup

Navigate to the backend:
```bash
cd backend
```

Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Set up environment variables:
```bash
cp .env.example .env
```
Fill in your `GROQ_API_KEY`, `PINECONE_API_KEY`, and `PINECONE_INDEX_NAME`.

Create the Pinecone index (if running for the first time):
```bash
python create_index.py
```

Run the backend server:
```bash
python main.py
# or: uvicorn main:app --reload --port 8000
```

Run the backend test suite:
```bash
pytest -v
```

---

#### 2. Frontend Setup

Open a new terminal window:
```bash
cd med-ai-frontend
```

Set up environment variables:
```bash
cp .env.example .env.local
```
Add your Clerk keys from the [Clerk Dashboard](https://dashboard.clerk.com).

Install dependencies:
```bash
npm install
```

Start the Next.js development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

# 💡 Example Use Case

A user uploads a medical report:

```text
Blood_Test_Report.pdf
```

The system processes and indexes the document.

The user can then ask:

```text
"What is my hemoglobin level?"
```

The RAG pipeline retrieves the relevant section from the uploaded document and provides a response based on that context.

The user can continue:

```text
"Is that within the normal range?"
```

Because conversation history is maintained, the assistant can understand that **"that" refers to the previously discussed hemoglobin value**.

---

## 📸 Screenshots & UI Previews

<div align="center">
  <img width="900" alt="Chat Interface" src="https://github.com/user-attachments/assets/f6b8aeb1-0bc8-49e3-b955-76e93f6552b8" />
  <p><em>Interactive Medical AI Chat Interface with Context Grounding</em></p>
</div>

<div align="center">
  <img width="900" alt="Session History" src="https://github.com/user-attachments/assets/42da07ac-d271-491a-ac62-f347ffe291ae" />
  <p><em>Document Ingestion & Multi-Session History</em></p>
</div>

<div align="center">
  <img width="900" alt="Authentication View" src="https://github.com/user-attachments/assets/586f570f-0d83-4aef-aa29-92ff488c4c14" />
  <p><em>Secure Authentication Flow powered by Clerk</em></p>
</div>

<div align="center">
  <img width="900" alt="Document Q&A" src="https://github.com/user-attachments/assets/9de17237-4b14-498b-a404-23b6a245723d" />
  <p><em>Context-Aware Follow-up Medical Consultation</em></p>
</div>

---

# 🔒 Security & Privacy

This project is designed with user-specific access and authentication in mind.

* Authentication handled through Clerk.
* User conversations are separated through application-level session handling.
* API keys are stored through environment variables.
* Sensitive configuration should never be committed to the repository.
* Medical information should be treated as sensitive data.

> **Disclaimer:** This project is intended for educational and demonstration purposes. It is not a substitute for professional medical diagnosis, treatment, or medical advice.

---

# 🎯 Why This Project?

This project demonstrates the combination of several modern Generative AI concepts into a complete application:

```text
LLMs
 │
 ├── RAG
 │    ├── Document Ingestion
 │    ├── Chunking
 │    ├── Embeddings
 │    └── Vector Search
 │
 ├── Agentic AI
 │    ├── LangGraph
 │    ├── State Management
 │    └── Workflow Routing
 │
 ├── Memory
 │    └── Conversation History
 │
 └── Full-Stack Engineering
      ├── Next.js
      ├── Python
      ├── Authentication
      └── Database
```

The goal is to demonstrate how **Generative AI, RAG, Agentic AI, and full-stack development** can be combined to build a practical AI application.

---

# 🚧 Roadmap & Improvements

* [x] **Automated Testing**: Unit test suite using `pytest` for chat storage and API endpoints
* [x] **Containerization**: Multi-service `docker-compose` orchestration for backend and frontend
* [x] **CI/CD Pipeline**: GitHub Actions for automated linting, test runs, and validation
* [ ] Multi-document reasoning & cross-document synthesis
* [ ] Advanced hybrid search (combining dense vector search + BM25)
* [ ] Source/page citations in LLM responses
* [ ] Streaming AI responses via WebSockets / SSE
* [ ] Observability and AI tracing (LangSmith / OpenTelemetry)

---

# 👨‍💻 Maintainer

**Rahil Netipattu**
* GitHub: [@nrahil](https://github.com/nrahil)
* Email: [netipatturahil@gmail.com](mailto:netipatturahil@gmail.com)

---

# 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

*Acknowledgments: Inspired by open-source RAG architectures and medical assistant reference designs.*
