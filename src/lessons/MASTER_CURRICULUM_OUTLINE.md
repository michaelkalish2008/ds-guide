# Master Data Science Curriculum Outline
## Using Cheese Manufacturing Database

## Topic
Comprehensive data science curriculum leveraging real-world manufacturing data to teach fundamental and advanced analytics skills through hands-on experience with a complete supply chain dataset, with a focus on LLM literacy and responsible AI development.

## Summary
This curriculum provides a structured learning path through 24 comprehensive lessons organized into 10 phases, each lesson designed as a focused 10-minute video format. Progressing from LLM literacy and responsible AI practices to advanced statistical analysis, machine learning systems, and comprehensive testing strategies. Each lesson uses the cheese manufacturing database - a 45MB SQLite database containing 200K+ records across 50+ tables representing the complete manufacturing pipeline from raw materials to final distribution.

The curriculum is designed to build skills incrementally, with each 10-minute lesson focusing on one core concept while building upon previous knowledge. Students work with real-world complexity including time-series data, categorical variables, quality control metrics, and business performance indicators, while developing critical thinking skills for AI-powered workflows.

## Objectives
By the end of this curriculum, students will be able to:

### **LLM Literacy & Responsible AI**
- Understand transformer architecture and attention mechanisms
- Apply critical thinking when working with LLMs
- Recognize bias, verify information, and use AI responsibly
- Comprehend vector spaces and language embeddings

### **Development Foundation**
- Master command line operations and environment management
- Set up professional development environments
- Manage Python dependencies and virtual environments
- Use Git for version control and collaboration

### **Essential Languages & Tools**
- Navigate file systems and manage files using UNIX commands
- Write bash scripts and set up cronjobs for automation
- Use Python for data processing and analysis
- Write SQL queries for database operations
- Integrate multiple languages in workflows

### **Data Pipeline Mastery**
- Perform advanced SQL queries and data extraction
- Execute comprehensive pandas operations and data transformations
- Clean and preprocess data for AI applications
- Build robust data pipelines

### **GenAI Implementation**
- Build and deploy AI agents using LangChain
- Connect AI systems to structured data sources
- Manage API keys and environment variables securely
- Create basic chat interfaces and Q&A systems

### **Text & Pattern Analysis**
- Process and analyze text data with advanced NLP techniques
- Extract patterns using regex and machine learning
- Implement classification, clustering, and recommendation systems
- Apply statistical methods to text analysis

### **Advanced AI Systems**
- Implement retrieval-augmented generation (RAG) systems
- Build multi-agent workflows and complex AI systems
- Fine-tune models for domain-specific applications
- Deploy production-ready AI applications

### **Statistical Analysis & Inference**
- Apply statistical methods to model evaluation and validation
- Conduct hypothesis testing and confidence interval analysis
- Perform A/B testing and experimental design
- Evaluate model performance using statistical rigor

### **Machine Learning Pipeline**
- Prepare and preprocess data for machine learning
- Engineer features and select appropriate algorithms
- Train, validate, and deploy ML models
- Implement MLOps and production ML systems

### **Testing & Quality Assurance**
- Write comprehensive tests using pytest and Jest
- Implement test-driven development practices
- Use testing for context enhancement and productivity
- Ensure code quality and reliability

## Curriculum Structure & Phases

### **Phase 1: LLM Literacy & Responsible AI (Lessons 1-3) - 10%**
- **Lesson 1**: What is an LLM? (Attention Mechanisms) - 10 min
- **Lesson 2**: Critical Thinking with LLMs - 10 min
- **Lesson 3**: Language as Mathematics (Vector Spaces) - 10 min

### **Phase 2: Development Foundation (Lessons 4-5) - 7%**
- **Lesson 4**: Terminal & Development Environment - 10 min
- **Lesson 5**: Python Environment Management - 10 min

### **Phase 3: Languages & Command Line (Lessons 6-8) - 12%**
- **Lesson 6**: Bash & UNIX Command Line - 10 min
- **Lesson 7**: Python Programming Fundamentals - 10 min
- **Lesson 8**: SQL Fundamentals - 10 min

### **Phase 4: Data Analysis (Lessons 9-10) - 10%**
- **Lesson 9**: Getting the Data (SQL) - 10 min
- **Lesson 10**: Cleaning the Data (Pandas) - 10 min

### **Phase 5: GenAI Implementation (Lessons 11-12) - 8%**
- **Lesson 11**: Your First AI Agent - 10 min
- **Lesson 12**: AI + Data Connection - 10 min

### **Phase 6: Natural Language Processing (Lessons 13-15) - 12%**
- **Lesson 13**: Understanding Text (NLP) - 10 min
- **Lesson 14**: Pattern Matching (Regex) - 10 min
- **Lesson 15**: Finding Patterns (ML) - 10 min

### **Phase 7: Advanced GenAI (Lessons 16-18) - 12%**
- **Lesson 16**: Advanced AI Systems (RAG) - 10 min
- **Lesson 17**: Multi-Agent Workflows - 10 min
- **Lesson 18**: Model Fine-tuning & Customization - 10 min

### **Phase 8: Statistics & Trust (Lesson 19) - 6%**
- **Lesson 19**: Trusting Your Results (Statistical Inference) - 10 min

### **Phase 9: Machine Learning (Lessons 20-22) - 10%**
- **Lesson 20**: Data Preparation & Feature Engineering - 10 min
- **Lesson 21**: Model Development & Training - 10 min
- **Lesson 22**: Model Evaluation & Deployment - 10 min

### **Phase 10: Testing & Quality Assurance (Lessons 23-24) - 13%**
- **Lesson 23**: Python Testing with Pytest - 10 min
- **Lesson 24**: JavaScript Testing with Jest & Vibe Coding - 10 min

## Common DS Applications

### **Quality Control & Predictive Analytics**
- **Application**: Predict quality test outcomes based on manufacturing parameters
- **Tables Used**: `quality_tests`, `cheese_manufacturing_batches`, `aging_lots`
- **Skills**: Classification models, feature engineering, model evaluation
- **Business Value**: Reduce quality issues, optimize production parameters

### **Process Optimization & Yield Management**
- **Application**: Analyze yield percentages and identify optimization opportunities
- **Tables Used**: `weighing_pricing`, `manufacturing_batches`, `aging_lots`
- **Skills**: Regression analysis, optimization algorithms, cost-benefit analysis
- **Business Value**: Increase yield, reduce waste, improve profitability

### **Environmental Monitoring & Time Series Analysis**
- **Application**: Monitor aging conditions and predict optimal aging duration
- **Tables Used**: `environmental_monitoring`, `aging_lots`, `temperature_monitoring`
- **Skills**: Time series analysis, forecasting, anomaly detection
- **Business Value**: Optimize aging conditions, reduce spoilage, ensure quality

### **Supply Chain Analytics & Logistics**
- **Application**: Analyze shipping performance and optimize logistics
- **Tables Used**: `shipments`, `temperature_monitoring`, `packaging_operations`
- **Skills**: Network analysis, optimization, performance metrics
- **Business Value**: Reduce shipping costs, improve delivery reliability

### **Sensory Analysis & Product Development**
- **Application**: Analyze sensory evaluation data for product improvement
- **Tables Used**: `sensory_evaluations`, `sensory_attributes`, `quality_tests`
- **Skills**: Statistical analysis, correlation studies, hypothesis testing
- **Business Value**: Improve product quality, guide product development

### **Regulatory Compliance & Traceability**
- **Application**: Implement FSMA 204 compliance and traceability systems
- **Tables Used**: `traceability_lot_codes`, `lot_master`, `batch_genealogy`
- **Skills**: Data governance, regulatory reporting, audit trails
- **Business Value**: Ensure compliance, reduce regulatory risk

## Detailed Lesson Outline

### **Phase 1: LLM Literacy & Responsible AI**

#### **Lesson 1: What is an LLM? (Attention Mechanisms) - 10 min**
- **Topic**: Understanding transformers, attention, how LLMs actually work
- **Summary**: Deep dive into transformer architecture and attention mechanisms in a focused 10-minute format
- **Objectives**: Understand transformer architecture, attention mechanisms, tokenization, model training
- **Common DS Applications**: Foundation for all AI applications, understanding model limitations
- **Outline**: Attention mechanisms (3 min), transformer architecture (4 min), LLM processing (3 min)

#### **Lesson 2: Critical Thinking with LLMs - 10 min**
- **Topic**: Responsible use, bias awareness, fact-checking
- **Summary**: Learn responsible AI practices and critical thinking with LLMs in a focused format
- **Objectives**: Recognize AI bias, verify information, use AI responsibly, understand limitations
- **Common DS Applications**: All AI applications, quality assurance, ethical AI development
- **Outline**: Understanding AI bias (3 min), fact-checking techniques (4 min), responsible practices (3 min)

#### **Lesson 3: Language as Mathematics (Vector Spaces) - 10 min**
- **Topic**: How language becomes numbers, embeddings, semantic similarity
- **Summary**: Understanding vector spaces and embeddings in a focused 10-minute format
- **Objectives**: Understand embeddings, vector spaces, semantic similarity, dimensionality reduction
- **Common DS Applications**: RAG systems, semantic search, recommendation systems
- **Outline**: Language to numbers (3 min), semantic similarity (4 min), practical applications (3 min)

### **Phase 2: Development Foundation**

#### **Lesson 4: Terminal & Development Environment - 10 min**
- **Topic**: Terminal navigation, file operations, IDE setup
- **Summary**: Master command line operations and set up professional development environment
- **Objectives**: Terminal navigation, file operations, IDE setup, command line confidence
- **Common DS Applications**: Environment reproducibility, automation, deployment
- **Outline**: Command line basics (3 min), file operations (4 min), IDE setup (3 min)

#### **Lesson 5: Python Environment Management - 10 min**
- **Topic**: Virtual environments with uv, dependency management, Git basics
- **Summary**: Set up professional Python development environment with modern tools
- **Objectives**: Virtual environment management, dependency management, Git workflows
- **Common DS Applications**: Project management, collaboration, deployment
- **Outline**: Virtual environments (3 min), dependency management (4 min), Git basics (3 min)

### **Phase 3: Languages & Command Line**

#### **Lesson 6: Bash & UNIX Command Line - 10 min**
- **Topic**: File system navigation, text processing, bash scripting
- **Summary**: Learn essential UNIX commands and bash scripting for data science automation
- **Objectives**: Navigate file systems, process text with grep/sed/awk, write bash scripts, set up cronjobs
- **Common DS Applications**: File management, text processing, workflow automation
- **Outline**: File system navigation (3 min), text processing tools (4 min), bash scripting (3 min)

#### **Lesson 7: Python Programming Fundamentals - 10 min**
- **Topic**: Python basics, data structures, libraries for data science
- **Summary**: Learn Python programming fundamentals for data manipulation and analysis
- **Objectives**: Write Python scripts, use data structures, implement file I/O, integrate with other tools
- **Common DS Applications**: Data processing, automation, analysis
- **Outline**: Python syntax (3 min), data structures (4 min), libraries (3 min)

#### **Lesson 8: SQL Fundamentals - 10 min**
- **Topic**: Database operations, querying, joins and aggregations
- **Summary**: Learn SQL for data extraction and analysis from manufacturing databases
- **Objectives**: Write SQL queries, use joins and aggregations, optimize performance, handle large datasets
- **Common DS Applications**: Data extraction, reporting, analysis
- **Outline**: SQL basics (3 min), joins and aggregations (4 min), performance optimization (3 min)

### **Phase 4: Data Analysis**

#### **Lesson 9: Getting the Data (SQL) - 10 min**
- **Topic**: Extract data from databases, SQL fundamentals
- **Summary**: Learn SQL to extract manufacturing data for AI applications
- **Objectives**: SQL proficiency, data extraction, database querying
- **Common DS Applications**: Data extraction, reporting, relationship analysis
- **Outline**: SQL basics (3 min), complex queries (4 min), data extraction (3 min)

#### **Lesson 10: Cleaning the Data (Pandas) - 10 min**
- **Topic**: Data preprocessing, transformation, cleaning
- **Summary**: Clean and preprocess data for optimal AI performance
- **Objectives**: Data cleaning, preprocessing, transformation, quality assurance
- **Common DS Applications**: Data engineering, quality assurance, preprocessing
- **Outline**: Data cleaning (3 min), preprocessing (4 min), quality checks (3 min)

### **Phase 5: GenAI Implementation**

#### **Lesson 11: Your First AI Agent - 10 min**
- **Topic**: Simple LangChain instantiation, API key management
- **Summary**: Build your first AI agent using LangChain ecosystem
- **Objectives**: LangChain basics, API key management, basic chat interface
- **Common DS Applications**: AI assistants, chatbots, automated workflows
- **Outline**: LangChain setup (3 min), API management (4 min), basic agent creation (3 min)

#### **Lesson 12: AI + Data Connection - 10 min**
- **Topic**: Connect LangChain to structured data, basic Q&A
- **Summary**: Connect AI agents to CSV data and build basic Q&A systems
- **Objectives**: Data integration, Q&A systems, structured data processing
- **Common DS Applications**: Data analysis automation, business intelligence
- **Outline**: Data integration (3 min), Q&A systems (4 min), structured data processing (3 min)

### **Phase 6: Natural Language Processing**

#### **Lesson 13: Understanding Text (NLP) - 10 min**
- **Topic**: Text processing, sentiment analysis, text classification
- **Summary**: Process manufacturing documents and text data with NLP techniques
- **Objectives**: Text preprocessing, sentiment analysis, text classification
- **Common DS Applications**: Document analysis, quality reports, customer feedback
- **Outline**: Text preprocessing (3 min), sentiment analysis (4 min), classification (3 min)

#### **Lesson 14: Pattern Matching (Regex) - 10 min**
- **Topic**: Extract structured information from messy text
- **Summary**: Use regex to extract and standardize data for AI applications
- **Objectives**: Regex patterns, text extraction, data standardization
- **Common DS Applications**: Data cleaning, information extraction, standardization
- **Outline**: Regex basics (3 min), pattern matching (4 min), text extraction (3 min)

#### **Lesson 15: Finding Patterns (ML) - 10 min**
- **Topic**: Train models on manufacturing data, classification, clustering
- **Summary**: Apply machine learning to manufacturing data for pattern recognition
- **Objectives**: Classification, clustering, recommendation systems, model evaluation
- **Common DS Applications**: Quality prediction, process optimization, recommendations
- **Outline**: Classification models (3 min), clustering (4 min), evaluation (3 min)

### **Phase 7: Advanced GenAI**

#### **Lesson 16: Advanced AI Systems (RAG) - 10 min**
- **Topic**: Retrieval-augmented generation, vector databases
- **Summary**: Build RAG systems that search and synthesize manufacturing information
- **Objectives**: RAG systems, vector databases, information retrieval, synthesis
- **Common DS Applications**: Intelligent search, knowledge management, Q&A systems
- **Outline**: RAG architecture (3 min), vector databases (4 min), retrieval systems (3 min)

#### **Lesson 17: Multi-Agent Workflows - 10 min**
- **Topic**: Complex agentic systems, multiple AI agents
- **Summary**: Build complex multi-agent systems for manufacturing analytics
- **Objectives**: Multi-agent systems, workflow orchestration, agent coordination
- **Common DS Applications**: Complex analytics, automation, decision support
- **Outline**: Multi-agent architecture (3 min), workflow orchestration (4 min), agent coordination (3 min)

#### **Lesson 18: Model Fine-tuning & Customization - 10 min**
- **Topic**: Fine-tuning models for domain-specific applications
- **Summary**: Learn to fine-tune models for manufacturing-specific language and tasks
- **Objectives**: Fine-tuning techniques, domain-specific training, model customization
- **Common DS Applications**: Manufacturing AI models, specialized applications
- **Outline**: Fine-tuning fundamentals (3 min), manufacturing-specific fine-tuning (4 min), production deployment (3 min)

### **Phase 8: Statistics & Trust**

#### **Lesson 19: Trusting Your Results (Statistical Inference) - 10 min**
- **Topic**: Model confidence, A/B testing, statistical inference
- **Summary**: Evaluate AI model performance and confidence using statistical methods
- **Objectives**: Statistical inference, model evaluation, confidence intervals, A/B testing
- **Common DS Applications**: Model validation, quality assurance, decision making
- **Outline**: Statistical inference (3 min), confidence intervals (4 min), model evaluation (3 min)

### **Phase 9: Machine Learning**

#### **Lesson 20: Data Preparation & Feature Engineering - 10 min**
- **Topic**: Preparing manufacturing data for machine learning
- **Summary**: Learn to clean, preprocess, and engineer features for ML algorithms
- **Objectives**: Data preprocessing, feature engineering, feature selection, dimensionality reduction
- **Common DS Applications**: All ML applications, data quality assurance
- **Outline**: Data cleaning and preprocessing (3 min), feature engineering techniques (4 min), advanced feature engineering (3 min)

#### **Lesson 21: Model Development & Training - 10 min**
- **Topic**: Choosing and training ML algorithms for manufacturing problems
- **Summary**: Learn to select and implement ML algorithms for different types of problems
- **Objectives**: Model selection, training and validation, advanced ML techniques
- **Common DS Applications**: Quality prediction, demand forecasting, predictive maintenance
- **Outline**: Model selection and algorithms (3 min), model training and validation (4 min), advanced ML techniques (3 min)

#### **Lesson 22: Model Evaluation & Deployment - 10 min**
- **Topic**: Evaluating models and deploying them in production
- **Summary**: Learn to evaluate model performance and deploy ML models in production
- **Objectives**: Model evaluation and interpretability, model deployment, ML pipeline automation
- **Common DS Applications**: Production ML systems, automated decision making
- **Outline**: Model evaluation and interpretability (3 min), model deployment (4 min), ML pipeline automation (3 min)

### **Phase 10: Testing & Quality Assurance**

#### **Lesson 23: Python Testing with Pytest - 10 min**
- **Topic**: Comprehensive Python testing using pytest framework
- **Summary**: Learn to write comprehensive tests for data science applications using pytest
- **Objectives**: Pytest fundamentals, advanced features, data science testing
- **Common DS Applications**: Data processing, ML models, ETL pipelines
- **Outline**: Pytest fundamentals (3 min), advanced features (4 min), data science testing (3 min)

#### **Lesson 24: JavaScript Testing with Jest & Vibe Coding - 10 min**
- **Topic**: JavaScript testing with Jest and vibe coding practices
- **Summary**: Learn Jest testing framework and vibe coding for enhanced productivity
- **Objectives**: Jest testing, vibe coding, context enhancement, quality assurance
- **Common DS Applications**: Web applications, API testing, productivity enhancement
- **Outline**: Jest fundamentals (3 min), web application testing (4 min), vibe coding (3 min)

## Technology Stack

### **Core Technologies**
- **Python 3.11+** - Primary programming language
- **SQLite** - Database management
- **Jupyter Notebooks** - Interactive development
- **Git** - Version control

### **Key Libraries**
- **Data Manipulation**: pandas, numpy
- **Visualization**: matplotlib, seaborn, altair
- **Machine Learning**: scikit-learn, SHAP, XGBoost, LightGBM
- **Statistics**: scipy, statsmodels
- **NLP**: NLTK, spaCy, transformers
- **AI/LLM**: LangChain, LangGraph, LangSmith
- **Vector Databases**: Chroma, Pinecone, Weaviate
- **Testing**: pytest

### **Development Tools**
- **Environment Management**: uv
- **Code Quality**: black, flake8
- **Documentation**: Jupyter notebooks, markdown

---

## Assessment Framework

### **Knowledge Checkpoints**
- **Phase 1**: LLM literacy and responsible AI practices
- **Phase 2**: Development environment mastery
- **Phase 3**: Language and command-line proficiency
- **Phase 4**: Data pipeline and preprocessing proficiency
- **Phase 5**: Basic AI agent implementation
- **Phase 6**: Text analysis and pattern recognition
- **Phase 7**: Advanced AI systems and multi-agent workflows
- **Phase 8**: Statistical analysis and model validation
- **Phase 9**: Machine learning pipeline development and deployment
- **Phase 10**: Testing and quality assurance implementation

### **Project Milestones**
- **Milestone 1**: Basic AI agent with data connection (Lesson 12)
- **Milestone 2**: Text analysis and pattern recognition system (Lesson 15)
- **Milestone 3**: Complete multi-agent manufacturing analytics system (Lesson 17)
- **Milestone 4**: Statistical validation and model trust assessment (Lesson 19)
- **Milestone 5**: Complete ML pipeline with deployment (Lesson 22)
- **Milestone 6**: Comprehensive testing and quality assurance (Lesson 24)

---

## Success Metrics

### **Technical Competencies**
- [ ] LLM literacy and responsible AI practices
- [ ] Development environment mastery
- [ ] Language and command-line proficiency
- [ ] AI agent implementation and data integration
- [ ] Data pipeline and preprocessing proficiency
- [ ] Text analysis and pattern recognition
- [ ] Advanced AI systems and multi-agent workflows
- [ ] Statistical analysis and model validation
- [ ] Machine learning pipeline development and deployment
- [ ] Testing and quality assurance implementation
- [ ] Production workflow deployment

### **Business Applications**
- [ ] Quality prediction models with AI integration
- [ ] Process optimization with multi-agent systems
- [ ] Document analysis and classification
- [ ] Natural language data interfaces
- [ ] Automated reporting systems
- [ ] Complex manufacturing analytics workflows
- [ ] Statistically validated decision support systems
- [ ] Production ML systems and MLOps
- [ ] Quality-assured and tested applications
- [ ] Reliable and maintainable code systems

---

*This curriculum is designed to provide hands-on experience with real-world data science challenges while building a comprehensive skill set applicable to manufacturing and business analytics domains, with a focus on modern AI-powered workflows, responsible AI practices, statistical rigor, production-ready systems, and comprehensive testing strategies. Each lesson is optimized for 10-minute video format to maximize engagement and learning efficiency.* 