# ds-guide
The Data Science (DS) Guide is here to help you learn and apply DS concepts and tools. If you are using Cursor, you can ask questions in your side bar (use **command l** shortcut).

## Structure

1. We'll kick off with creating a virtual environment (alias venv) for installing all of the packages we'll need. We'll be running the following command to install the packages listed in requirements.txt
```bash
uv init
uv add -r requirements.txt
uv sync
```
2. The .env file is our "hidden" file containing our API keys. These are to be kept secret and not stored in Github. Go to OpenAI, LangSmith, Supabase, etc. to get your keys!
3. Configurations and settings apply generally to the repo and so will be stored in config.yaml and settings.py.
4. .gitignore (another "hidden" file) ensures that certain files are not uploaded to Github.
5. This repo follows the convention of locating code in a source (src) directory.

Below is layout of the repo:

├── src/
│   ├── lessons/
│   │   ├── phase1_llm_literacy/      # LLM Literacy & Responsible AI
│   │   ├── phase2_development/        # Development Foundation
│   │   ├── phase3_genai/             # GenAI Implementation
│   │   ├── phase4_data_pipeline/     # Data Pipeline (SQL & Pandas)
│   │   ├── phase5_text_patterns/     # Text & Patterns (NLP & ML)
│   │   ├── phase6_advanced_ai/       # Advanced AI Systems
│   │   └── phase7_stats/             # Statistics & Trust
│   ├── database/
│   │   ├── config/
│   │   ├── db/
│   │   ├── docs/
│   │   ├── quick_start.py
│   │   ├── README.md
│   │   ├── scripts/
│   │   └── tests/
│   ├── platforms-tools/
│   ├── languages-commands/
│   ├── packages/
│   ├── file-types/
│   ├── statistics/
│   ├── genai-nlp/
│   ├── machine-learning/
│   └── graphs/
├── venv/                    # Virtual environment (created during setup)
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables and secrets
├── config.yaml              # Configuration settings
├── .gitignore              # Git ignore file
├── LICENSE                 # License for the repo on Github
└── README.md               # This file - your setup and overview guide

## Curriculum Overview

The curriculum is organized into 7 phases with 15 comprehensive lessons, using real-world manufacturing data to teach data science concepts:

### **Phase 1: LLM Literacy & Responsible AI (Lessons 1-3)**
- Understanding transformer architecture and attention mechanisms
- Critical thinking with LLMs and bias awareness
- Language as mathematics (vector spaces and embeddings)

### **Phase 2: Development Foundation (Lessons 4-5)**
- Terminal navigation and development environment setup
- Python environment management with modern tools

### **Phase 3: GenAI Implementation (Lessons 6-7)**
- Building your first AI agent with LangChain
- Connecting AI to structured data sources

### **Phase 4: Data Pipeline (Lessons 8-9)**
- SQL fundamentals for data extraction
- Pandas for data cleaning and preprocessing

### **Phase 5: Text & Patterns (Lessons 10-12)**
- Natural language processing techniques
- Pattern matching with regex
- Machine learning for pattern recognition

### **Phase 6: Advanced AI (Lessons 13-14)**
- Retrieval-augmented generation (RAG) systems
- Multi-agent workflows and complex AI systems

### **Phase 7: Statistics & Trust (Lesson 15)**
- Statistical inference and model validation
- A/B testing and confidence intervals

## Overview of sections

- **Platforms & Tools**: IDEs, databases, messaging systems, repositories, and dependency management
- **Languages & Commands**: Programming languages, text processing, queries, and web technologies
- **Packages**: Essential libraries for data science, ML, visualization, and analysis
- **File Types**: Understanding various data formats, code files, and configuration files

### Statistics
- Statistical schools of thought (Frequentist vs Bayesian)
- Complexity analysis and computational considerations
- Simulation methods (Markov chains, Monte Carlo)
- Probability distributions and their applications
- Statistical testing and experimental design
- Key statistical concepts and terminology

### Generative AI & NLP
- Transformer architecture fundamentals
- Neural network concepts (attention, embeddings, encodings)
- Natural language processing techniques
- Retrieval and similarity methods

### Machine Learning
- Model types and architectures
- Performance metrics and evaluation
- Model explainability and interpretability
- Training methodologies and best practices
- Data preprocessing and feature engineering

### Graph Theory
- Centrality measures and network analysis
- Graph features and community detection
- Network visualization and analysis techniques

## Getting Started

### Prerequisites Setup Notes

Before diving into data science, you'll need to set up your development environment. Here's a step-by-step guide. 

**Warning: Frustration.** If you are non-technical, this will be disorientating and painful. I highly recommend passing the following into an LLM for you to ask questions and to seek clarity! Below is a summary of the set up instructions by section:

1. **Check what you have.** If you already have a package manager, python and git, then you are ready to go! If not, we'll move forward.
2. **Install package manager.** The good news is that you won't have to prepare your computer from scratch. As stated on its website, "Homebrew installs the stuff you need that Apple (or your Linux system) didn’t." If you are new to DS, then you may be new to running commands in your Command Line Interface (CLI or "terminal"). When you follow our commands, you'll see a stream of text in your terminal, which can be nerve racking for the newcomer. These installations have been carefully designed to ensure compatibility and functionality. You don't need to read everything, but keep an eye out for disclaimers, notes and requested actions. While installing homebrew and git might be a one-time-thing, you may need to run --update and --upgrade whenever homebrew makes a change. 
3. **Install git and github cli.** If you have cloned the ds-guide, you'll need these tools to work with the repository. You might want to:
   - **Make your own copy** (called "forking") if you plan to maintain your own version
   - **Create a branch** if you want to contribute improvements back to the original
   - **Clone and modify locally** if you just want to learn and experiment 
4. **Install python.** Instructions involve installing via homebrew.
5. **Create a virtual environment.** In our case, we use the alias "venv" for our virtual environment. You'll need to activate your venv and you can deactivate/reactivate as needed (for example, if you close your terminal, you'll need to reactivate. The venv will be used to install the remainder of packages. If something goes wrong, delete the venv and create a new one! If you were to try to maintain all of your python packages globally, you might run into conflicts later on across your projects. This is a way for you to localize your dependency management to the ds-guide.
6. **Install Required Packages.** Run a quick command to install all of the necessary python packages.
7. **Verify Your Setup.** Confirm your setup by checking your installations.

#### 1. Check Your Current Setup

First, let's see what you already have installed:

```bash
# Check if Python is installed
python3 --version
# or
python --version

# Check if Git is installed
git --version

# Check if Homebrew is installed
brew --version
```

#### 2. Install Homebrew

Homebrew is macOS/Linux's package manager. If you don't already have homebrew, you can download it from their [website](https://brew.sh/).

**Using Homebrew (macOS/Linux)**

```bash
# If you don't already have homebrew, here is the command from their website. Just copy-paste it into your terminal and hit enter and follow the installation instructions.
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# If you already have homebrew or think you might have it, use:
brew update

# If their are outstanding updates, follow the instructions:
brew upgrade
```

#### 3. Install Git & GitHub CLI

**Git** is the version control system that GitHub uses. You'll need this to work with code repositories.

**Using Homebrew (macOS/Linux)**
```bash

# First check if you already have git
which git

# Install Git
brew install git

# Install GitHub CLI (optional but recommended)
brew install gh
```

**Set up Git (first time only):**
```bash
# Configure your identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name
git config --global init.defaultBranch main
```

**GitHub CLI Setup (optional):**
```bash
# Authenticate with GitHub (learn more about the CLI [here](https://cli.github.com/))
gh auth login

# Follow the prompts to authenticate via browser or token
# If you are new to GitHub, the workflow may not be familiar to you. Feel free to return to this step at a future point in your career.
```

### Repository Workflow Options

Depending on your goals, you have several options for working with this guide:

#### Option A: Make Your Own Copy (Fork)
If you want to maintain your own version of this guide:
```bash
# On GitHub, click the "Fork" button (this creates your own copy)
# Then clone your copy to your computer
# Replace "YOUR_USERNAME" with your actual GitHub username
gh repo clone YOUR_USERNAME/ds-guide
# or
git clone https://github.com/YOUR_USERNAME/ds-guide.git
```

#### Option B: Contribute Improvements
If you want to suggest improvements to the original guide:
```bash
# Clone the original repository to your computer
# Replace "ORIGINAL_USERNAME" with the actual GitHub username (e.g., "michaelkalish")
gh repo clone ORIGINAL_USERNAME/ds-guide
# or
git clone https://github.com/ORIGINAL_USERNAME/ds-guide.git

# Create a new branch (like a separate workspace) for your changes
git checkout -b feature/your-improvement-name

# Make your changes, then create a pull request (suggest your changes)
git add .
git commit -m "Add your improvement description"
git push origin feature/your-improvement-name
# Then use GitHub CLI or website to create a pull request
```

#### Option C: Learn and Experiment
If you just want to learn and don't need version control:
```bash
# Clone and work locally without pushing changes
# Replace "ORIGINAL_USERNAME" with the actual GitHub username (e.g., "michaelkalish")
git clone https://github.com/ORIGINAL_USERNAME/ds-guide.git
cd ds-guide
# Make changes locally for learning purposes
```

#### 4. Install Python

**Using Homebrew (macOS/Linux)**
```bash
# Use the following command to check your python folder/version
which python3

# If you don't already have Python, install Python
brew install python
```

#### 5. Set Up Your Project Environment

Once Python is installed, create a virtual environment for this project. For ference, we are using this guidance: https://docs.python.org/3.12/tutorial/venv.html 

```bash
# Navigate to your project directory
cd /path/to/your/ds-guide

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Your prompt should now show (venv) indicating the virtual environment is active
```

#### 6. Install Required Packages

```bash
# Make sure your virtual environment is activated
pip install --upgrade pip

# Install all required packages from requirements.txt
pip install -r requirements.txt

# If you want to install data science packages individually, you can use the following syntax
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

#### 7. Verify Your Setup

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Test basic imports
python -c "import pandas as pd; import numpy as np; print('Setup successful!')"
```

### Troubleshooting

**If you get "command not found" errors:**
- Make sure Python is in your PATH
- Try using `python3` instead of `python`
- Restart your terminal after installation

**If you can't install Homebrew:**
- Check your macOS version (Homebrew requires macOS 10.14 or later)
- Ensure you have administrator privileges
- Try the manual installation from [brew.sh](https://brew.sh)

**If virtual environment creation fails:**
- Make sure you have write permissions in the directory
- Try creating the venv in a different location
- Check if your Python installation includes venv module