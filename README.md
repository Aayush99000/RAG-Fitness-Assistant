# 💪 Fitness RAG Assistant

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![RAG](https://img.shields.io/badge/RAG-Powered-orange.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**An AI-powered fitness assistant using Retrieval Augmented Generation (RAG) to provide personalized workout plans, exercise recommendations, and form guidance.**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Architecture](#architecture) • [Contributing](#contributing)

</div>

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [Examples](#examples)
- [How It Works](#how-it-works)
- [Development](#development)
- [Roadmap](#roadmap)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)

---

## 🎯 About

Fitness RAG Assistant is an intelligent chatbot that helps users with their fitness journey by providing:

- **Accurate exercise information** from a curated database
- **Personalized workout plans** based on user goals and equipment
- **Form and technique guidance** to prevent injuries
- **Equipment-specific recommendations** for home or gym workouts

Unlike generic fitness apps, this assistant uses **RAG (Retrieval Augmented Generation)** to ground its responses in verified fitness knowledge, ensuring accurate and safe recommendations.

---

## ✨ Features

### Core Capabilities

- 🏋️ **Exercise Database**: 500+ exercises with detailed instructions
- 📋 **Workout Generation**: Create customized workout plans
- ✅ **Form Guidance**: Step-by-step technique instructions
- 🎯 **Smart Filtering**: Filter by equipment, muscle group, difficulty
- 🩺 **Injury Awareness**: Recommendations considering injuries/limitations
- 💬 **Natural Conversation**: Chat interface for easy interaction

### Technical Features

- ⚡ **Fast Responses**: Powered by Groq's high-speed inference
- 🆓 **100% Free**: No API costs using open-source stack
- 🔒 **Privacy First**: Local vector database, no data sharing
- 📊 **Source Attribution**: See which documents informed each answer
- 🎨 **Modern UI**: Clean Streamlit interface

---

## 🛠️ Tech Stack

### AI & ML

- **LLM**: [Groq](https://groq.com/) (Llama 3 8B)
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector Database**: ChromaDB
- **Framework**: LangChain

### Backend & Frontend

- **Language**: Python 3.8+
- **UI**: Streamlit
- **Data Processing**: Pandas, NumPy

### Why This Stack?

- ✅ **Completely Free**: No API costs
- ✅ **Fast**: Groq provides lightning-fast inference
- ✅ **Local**: ChromaDB runs locally for privacy
- ✅ **Simple**: Easy to set up and maintain

---

## 📦 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed ([Download](https://www.python.org/downloads/))
- **Git** installed ([Download](https://git-scm.com/downloads))
- **Groq API Key** (free) - [Get it here](https://console.groq.com/keys)
- **8GB+ RAM** recommended
- **Internet connection** for initial setup

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/fitness-rag.git
cd fitness-rag
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Groq API key
# Use nano, vim, or any text editor
nano .env
```

Add your API key:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

### Step 5: Prepare Data

Add your fitness data to `data/raw/`:

```bash
# Example structure
data/raw/exercises.json
data/raw/articles/training_basics.txt
```

Sample `exercises.json` format:

```json
[
  {
    "name": "Barbell Squat",
    "category": "Legs",
    "muscle_groups": ["Quadriceps", "Glutes", "Hamstrings"],
    "equipment": "Barbell, Squat Rack",
    "difficulty": "Intermediate",
    "instructions": "Stand with feet shoulder-width apart...",
    "form_tips": "Keep chest up, knees track over toes..."
  }
]
```

### Step 6: Initialize Vector Database

```bash
python scripts/setup_vectordb.py
```

This will:

- Load all your fitness data
- Generate embeddings
- Populate ChromaDB
- Save locally to `chroma_db/`

### Step 7: Test the Setup

```bash
# Quick test
python scripts/test_query.py
```

---

## 📁 Project Structure

```
fitness-rag/
│
├── 📄 README.md                    # You are here!
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env                         # API keys (DO NOT COMMIT)
├── 📄 .env.example                 # Environment template
├── 📄 .gitignore                   # Git ignore rules
│
├── 📱 app.py                       # Streamlit web interface
├── 📱 main.py                      # CLI interface
│
├── 📂 data/                        # All data files
│   ├── raw/                        # Original data
│   │   ├── exercises.json
│   │   ├── workouts.json
│   │   └── articles/
│   └── processed/                  # Cleaned data
│
├── 📂 src/                         # Source code
│   ├── __init__.py
│   ├── config.py                   # Configuration settings
│   ├── data_loader.py              # Load and process data
│   ├── embeddings.py               # Generate embeddings
│   ├── vectorstore.py              # Vector DB operations
│   ├── llm.py                      # LLM interaction
│   └── rag_chain.py                # Complete RAG pipeline
│
├── 📂 scripts/                     # Utility scripts
│   ├── setup_vectordb.py           # Initialize vector DB
│   ├── scrape_data.py              # Data collection
│   └── test_query.py               # Quick testing
│
├── 📂 notebooks/                   # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_embedding_test.ipynb
│   └── 03_retrieval_test.ipynb
│
├── 📂 tests/                       # Unit tests
│   ├── __init__.py
│   └── test_retrieval.py
│
└── 📂 chroma_db/                   # Vector database (auto-generated)
```

---

## ⚙️ Configuration

### Environment Variables

Edit `.env` file to customize:

```bash
# LLM Settings
GROQ_API_KEY=your_key_here
LLM_MODEL=llama3-8b-8192           # Groq model
TEMPERATURE=0.7                     # Response creativity (0-1)

# Embedding Settings
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Retrieval Settings (in src/config.py)
TOP_K_RESULTS=5                     # Number of retrieved documents
CHUNK_SIZE=1000                     # Document chunk size
CHUNK_OVERLAP=200                   # Overlap between chunks
```

### Advanced Configuration

Edit `src/config.py` for more options:

```python
# System prompt
SYSTEM_PROMPT = """Your custom prompt here..."""

# Vector database
CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "fitness_knowledge"
```

---

## 🎮 Usage

### Web Interface (Recommended)

```bash
streamlit run app.py
```

Then open your browser to: `http://localhost:8501`

**Features:**

- 💬 Chat interface
- 📚 View source documents
- 🎨 Clean, modern UI
- 📱 Mobile responsive

### Command Line Interface

```bash
python main.py
```

**Example:**
