# 🐧 Welcome to Data Science!

Hey there, future data scientist! 👋

This guide is your friendly companion for learning data science using fun, real-world datasets. Whether you're completely new to coding or just new to data science, we've got you covered.

## What You'll Learn With 🎯

We'll explore data science using these interesting datasets:
- **🐧 Penguins** - Discover patterns in Antarctic penguin species
- **🚗 Cars** - Analyze automotive performance and specifications
- **💰 Tips** - Understand restaurant tipping patterns
- **✈️ Flights** - Investigate flight delays and performance

Don't worry if this sounds complex - we'll start simple and build up your skills step by step!

## Machine Learning Fundamentals 🤖

Want to understand how neural networks and deep learning really work? We've created a comprehensive series of notebooks that build your ML knowledge from the ground up:

### 📚 The Complete ML Series

1. **[Math Foundations](fundamentals/01_math_foundations.ipynb)** - Linear algebra, calculus, and probability essentials
   - Vectors, matrices, and operations
   - Derivatives and the chain rule
   - Softmax and probability distributions

2. **[Neural Network Basics](fundamentals/02_neural_network_basics.ipynb)** - Understanding the building blocks
   - Perceptrons and neurons
   - Activation functions (ReLU, sigmoid, tanh)
   - Forward propagation
   - Loss functions

3. **[Feedforward Networks](fundamentals/03_feedforward_networks.ipynb)** - Building complete networks
   - From scratch in NumPy
   - Modern implementation in PyTorch
   - Training on real datasets

4. **[Backpropagation](fundamentals/04_backpropagation.ipynb)** - The heart of deep learning
   - Computational graphs
   - Chain rule in action
   - Complete implementation with gradient checking
   - PyTorch autograd

5. **[Optimization](fundamentals/05_optimization.ipynb)** - Training neural networks effectively
   - Gradient descent variants
   - Momentum and Adam
   - Learning rate schedules
   - Regularization techniques

6. **[Attention Mechanisms](fundamentals/06_attention_mechanism.ipynb)** - Foundation of modern AI
   - Query, Key, Value paradigm
   - Scaled dot-product attention
   - Multi-head attention
   - Self-attention and transformers

**🎯 Each notebook includes:**
- Clear explanations with math
- Working code (NumPy + PyTorch)
- Visualizations
- Practice exercises

**💡 Perfect for:** Anyone who wants to truly understand how ChatGPT, GPT-4, and other modern AI systems work under the hood!

## Quick Start (5 minutes) ⚡

**Already have Python?** Jump right in:
```bash
git clone https://github.com/michaelkalish/ds-guide.git
cd ds-guide
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**New to programming?** No worries! Follow our [complete setup guide](#getting-started) below.

## How This Guide Works 📁

Think of this like organizing your digital workspace:

1. **📦 Virtual Environment** - Like having a clean, separate toolbox just for this project
2. **🔐 API Keys** - Your secret passwords for accessing AI services (we'll help you get these!)
3. **⚙️ Settings** - Project preferences stored in simple config files
4. **🚫 .gitignore** - Keeps your secrets and personal files private

Don't worry about the technical details yet - we'll walk through everything together!

## Getting Started 🚀

### Choose Your Path

**👩‍💻 I'm comfortable with computers** → Jump to [Quick Setup](#quick-setup)

**🆕 I'm new to programming** → Follow our [Step-by-Step Guide](#complete-setup-guide)

**🤔 Not sure which?** → Start with checking what you already have below!

---

### Quick Setup ⚡
*For those who already have Python, Git, and UV*

```bash
# 1. Get the code
git clone https://github.com/michaelkalish/ds-guide.git
cd ds-guide

# 2. Initialize and install everything with UV
uv init --no-readme
uv sync
uv add -r requirements.txt

# 3. Test it works
uv run python -c "import pandas; print('🎉 Ready to go!')"
```

---

### Complete Setup Guide 🛠️
*Don't worry - we'll go step by step!*

Think of this like setting up a new phone - it takes a few steps, but then everything works smoothly. Each step builds on the previous one, and we'll explain what each command does.

#### Step 1: Check What You Already Have 🔍

Let's see what's already installed on your computer:

```bash
# Check for Python (try both commands)
python3 --version
python --version

# Check for Git
git --version

# Check for Homebrew (Mac/Linux only)
brew --version
```

✅ **If you see version numbers, great! You can skip installing those tools.**

❌ **If you see "command not found", no worries - we'll install them next.**

#### Step 2: Install Homebrew (Mac/Linux) 🍺

Homebrew is like an app store for developer tools. It makes installing Python and Git super easy!

```bash
# Copy and paste this command (it's from the official Homebrew website)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# If you already have Homebrew, just update it
brew update && brew upgrade
```

💡 **Tip:** You'll see lots of text scrolling by - this is normal! Just wait for it to finish.

#### Step 3: Install Git 📝

Git helps you save and track changes to your code (like "save points" in a video game!).

```bash
# Install Git using Homebrew
brew install git

# Tell Git who you are (use your real name and email)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
```

🎯 **That's it for Git!** We'll skip the GitHub CLI for now - you can always add it later.

#### Step 4: Get This Guide on Your Computer 💾

Simply download the guide to your computer:

```bash
# Download the guide
git clone https://github.com/michaelkalish/ds-guide.git

# Go into the folder
cd ds-guide
```

🎉 **That's it!** You now have all the learning materials on your computer.

#### Step 5: Install Python & UV 🐍

Python is the programming language we'll use for data science, and UV is a fast Python package manager:

```bash
# Install Python using Homebrew
brew install python

# Install UV (fast Python package manager)
brew install uv

# Check they worked
python3 --version
uv --version
```

✅ **You should see version numbers for both Python (3.8+) and UV!**

#### Step 6: Create Your Workspace 🏗️

Think of this like creating a separate drawer for this project's tools:

```bash
# Make sure you're in the ds-guide folder
cd ds-guide

# Initialize the project with UV (this creates everything you need)
uv init --no-readme

# Sync your environment and install all packages
uv sync

# Add packages from requirements.txt
uv add -r requirements.txt
```

🚀 **UV is much faster than pip - this should only take 30-60 seconds!**

💡 **UV automatically creates and manages your virtual environment - no manual activation needed!**

#### Step 7: Test Everything Works ✅

Let's make sure everything is working:

```bash
# Test that Python can find your data science tools
uv run python -c "import pandas, numpy, matplotlib; print('🎉 Everything works! You are ready for data science!')"
```

🎊 **If you see the success message, congratulations! You're all set up.**

#### Step 8: Get Your Code Editor 👨‍💻

You'll need a code editor to write and run your data science code. We recommend these two excellent options:

**Option A: VS Code (Free & Popular) 🆓**
```bash
# Install VS Code using Homebrew
brew install --cask visual-studio-code

# Or download from: https://code.visualstudio.com/
```

**Option B: Cursor (AI-Powered, Great for Learning) 🤖**
```bash
# Install Cursor using Homebrew
brew install --cask cursor

# Or download from: https://cursor.com/
```

**💡 Which should you choose?**
- **New to programming?** → Cursor (it has built-in AI help!)
- **Want the most popular option?** → VS Code
- **Can't decide?** → Try Cursor first, you can always switch later

**Essential Extensions to Install:**
Once you have your editor, install these helpful extensions:
- Python (for Python support)
- Jupyter (for notebook files)
- Python Debugger (for debugging code)

---

## Need Help? 🆘

**Stuck on setup?** Don't worry - this happens to everyone! Here are quick fixes:

### Common Issues & Solutions

**❌ "command not found"**
- Try `python3` instead of `python`
- Restart your terminal and try again
- Make sure you installed the tool in the previous step

**❌ Can't install Homebrew**
- Make sure you're on macOS 10.14+ or Linux
- You might need admin/sudo privileges
- Visit [brew.sh](https://brew.sh) for manual installation

**❌ Virtual environment problems**
- Make sure you're in the `ds-guide` folder: `cd ds-guide`
- Try a different folder name: `python3 -m venv my-venv`
- Delete and recreate: `rm -rf venv` then try again

**❌ Package installation fails**
- Make sure you're in the ds-guide folder
- Try: `uv sync` to refresh everything
- If still stuck, try: `uv add pandas numpy matplotlib` to install core packages individually

**💡 Pro tip:** Copy error messages and ask ChatGPT or Claude for help! They're great at debugging setup issues.

---

## What's Next? 🎯

🎉 **You're all set up!** Here's how to start your data science journey:

### Getting Started with Your Projects

1. **📂 Open your project in your editor:**
   ```bash
   # If you chose VS Code
   code ds-guide

   # If you chose Cursor
   cursor ds-guide
   ```

2. **🐍 Select your Python environment:**
   - Look for "Select Interpreter" in your editor
   - Choose the one that shows `./venv/bin/python`

3. **📓 Start exploring:**
   - Open any `.ipynb` file to see interactive notebooks
   - Try running code cells with `Shift + Enter`
   - 🐧 Start with the penguin dataset examples

4. **💬 Use AI assistance (especially in Cursor):**
   - Ask questions about the code: "What does this function do?"
   - Get help with errors: "Why isn't this working?"
   - Request explanations: "Explain this visualization"

### Your First Steps
- **Beginners:** Start with basic data loading and simple plots
- **Intermediate:** Try data cleaning and statistical analysis
- **Advanced:** Experiment with machine learning models

**🚀 Ready to become a data scientist?** Open your editor and start exploring!