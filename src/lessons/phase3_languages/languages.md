# Phase 3: Languages & Command Line
## Essential Languages for Data Science

## Topic
Comprehensive introduction to essential languages and command-line tools for data science, covering bash scripting, UNIX commands, Python programming, and SQL fundamentals with practical applications to manufacturing data.

## Summary
This phase teaches students the fundamental languages and tools needed for data science work. Students learn bash scripting, UNIX command-line tools, Python programming basics, and SQL querying. The focus is on practical skills that enable efficient data manipulation, automation, and analysis using real-world manufacturing data.

## Objectives
By the end of this phase, students will be able to:

### **Bash & UNIX Command Line**
- Navigate file systems and manage files using UNIX commands
- Use grep, find, and other text processing tools
- Write basic bash scripts for automation
- Set up and manage cronjobs for scheduled tasks
- Handle special characters and text manipulation

### **Python Programming Fundamentals**
- Write basic Python scripts for data processing
- Use Python libraries for data manipulation
- Implement file I/O and data structures
- Create reusable functions and modules

### **SQL Database Operations**
- Write basic SQL queries for data extraction
- Use joins, aggregations, and filtering
- Connect to databases and execute queries
- Understand database schemas and relationships

### **Language Integration**
- Combine bash, Python, and SQL in workflows
- Automate data processing pipelines
- Handle different data formats and sources
- Create reproducible data science workflows

## Common DS Applications

### **Data Pipeline Automation**
- **Application**: Automate data collection and preprocessing workflows
- **Languages Used**: Bash, Python, SQL
- **Tools**: grep, find, sed, awk, pandas, sqlite3, cron
- **Business Value**: Reduce manual work, ensure data consistency

### **Scheduled Data Processing**
- **Application**: Set up automated data processing on schedules
- **Languages Used**: Bash, cron, Python
- **Tools**: cron, crontab, bash scripts, Python schedulers
- **Business Value**: Automated data updates, consistent processing

### **File Management & Organization**
- **Application**: Organize and manage large datasets and files
- **Languages Used**: Bash, UNIX commands
- **Tools**: ls, find, mv, cp, rm, tar, gzip
- **Business Value**: Efficient data organization, reduced storage costs

### **Text Processing & Analysis**
- **Application**: Process and analyze text-based manufacturing data
- **Languages Used**: Bash, Python, grep, sed
- **Tools**: grep, sed, awk, Python string methods
- **Business Value**: Extract insights from logs, reports, and documents

### **Database Operations**
- **Application**: Query and extract manufacturing data from databases
- **Languages Used**: SQL, Python
- **Tools**: SQLite, pandas, sqlalchemy
- **Business Value**: Efficient data access, automated reporting

## Lesson Outline

### **Lesson 8: Bash & UNIX Command Line**

#### **Part 1: File System Navigation**
- **Topic**: Navigating file systems and managing files
- **Summary**: Learn essential UNIX commands for file and directory management
- **Objectives**:
  - Navigate directories using cd, pwd, ls
  - Manage files with cp, mv, rm, mkdir
  - Understand file permissions and ownership
  - Use wildcards and special characters
- **Common DS Applications**: File organization, data management
- **Outline**:
  - Basic navigation commands (cd, pwd, ls)
  - File management (cp, mv, rm, mkdir)
  - File permissions and ownership
  - Wildcards and special characters

#### **Part 2: Text Processing Tools**
- **Topic**: Processing and manipulating text data
- **Summary**: Learn to use grep, sed, awk, and other text processing tools
- **Objectives**:
  - Search and filter text using grep
  - Edit text streams with sed
  - Process structured text with awk
  - Combine tools in pipelines
- **Common DS Applications**: Log analysis, data cleaning, text extraction
- **Outline**:
  - grep for pattern matching and searching
  - sed for stream editing
  - awk for text processing
  - Command pipelines and redirection

#### **Part 3: Bash Scripting & Automation**
- **Topic**: Writing bash scripts and setting up scheduled automation
- **Summary**: Learn to write bash scripts and set up cronjobs for automated data science workflows
- **Objectives**:
  - Write basic bash scripts
  - Use variables and control structures
  - Handle command-line arguments
  - Set up and manage cronjobs
  - Create scheduled automation scripts
- **Common DS Applications**: Workflow automation, batch processing, scheduled tasks
- **Outline**:
  - Bash script structure and syntax
  - Variables and control structures
  - Command-line argument handling
  - Cronjob setup and management
  - Scheduled task automation

### **Lesson 9: Python Programming Fundamentals**

#### **Part 1: Python Basics**
- **Topic**: Introduction to Python programming for data science
- **Summary**: Learn Python fundamentals for data manipulation and analysis
- **Objectives**:
  - Write basic Python scripts
  - Use data structures (lists, dictionaries, sets)
  - Implement control structures and functions
  - Handle file I/O operations
- **Common DS Applications**: Data processing, automation, analysis
- **Outline**:
  - Python syntax and data types
  - Data structures and collections
  - Control structures (if, for, while)
  - Functions and modules

#### **Part 2: Python for Data Science**
- **Topic**: Python libraries and tools for data science
- **Summary**: Learn to use Python libraries for data manipulation and analysis
- **Objectives**:
  - Use pandas for data manipulation
  - Work with numpy for numerical operations
  - Handle different data formats (CSV, JSON, XML)
  - Create data processing pipelines
- **Common DS Applications**: Data analysis, preprocessing, automation
- **Outline**:
  - pandas for data manipulation
  - numpy for numerical operations
  - File format handling (CSV, JSON, XML)
  - Data processing pipelines

#### **Part 3: Python Integration**
- **Topic**: Integrating Python with other tools and languages
- **Summary**: Learn to integrate Python with bash, SQL, and other tools
- **Objectives**:
  - Execute shell commands from Python
  - Connect to databases using Python
  - Create cross-language workflows
  - Handle errors and exceptions
- **Common DS Applications**: Multi-language workflows, automation
- **Outline**:
  - subprocess for shell command execution
  - Database connections (sqlite3, sqlalchemy)
  - Error handling and logging
  - Cross-language integration

### **Lesson 10: SQL Fundamentals**

#### **Part 1: SQL Basics**
- **Topic**: Introduction to SQL for data querying
- **Summary**: Learn basic SQL commands for querying and manipulating data
- **Objectives**:
  - Write basic SELECT queries
  - Use WHERE clauses for filtering
  - Apply ORDER BY and LIMIT
  - Understand basic data types
- **Common DS Applications**: Data extraction, reporting, analysis
- **Outline**:
  - SELECT statements and basic syntax
  - WHERE clauses and filtering
  - ORDER BY and LIMIT
  - Data types and constraints

#### **Part 2: SQL Joins and Aggregations**
- **Topic**: Advanced SQL operations for data analysis
- **Summary**: Learn to use joins, aggregations, and grouping for complex queries
- **Objectives**:
  - Use different types of JOINs
  - Apply aggregate functions (COUNT, SUM, AVG)
  - Use GROUP BY and HAVING
  - Create subqueries and CTEs
- **Common DS Applications**: Complex data analysis, reporting
- **Outline**:
  - JOIN types (INNER, LEFT, RIGHT, FULL)
  - Aggregate functions and GROUP BY
  - HAVING clauses and filtering
  - Subqueries and Common Table Expressions

#### **Part 3: SQL for Data Science**
- **Topic**: SQL techniques for data science applications
- **Summary**: Learn advanced SQL techniques for data science workflows
- **Objectives**:
  - Use window functions for analysis
  - Create views and temporary tables
  - Optimize query performance
  - Handle large datasets efficiently
- **Common DS Applications**: Advanced analytics, performance optimization
- **Outline**:
  - Window functions (ROW_NUMBER, RANK, LAG)
  - Views and temporary tables
  - Query optimization and indexing
  - Large dataset handling

## Hands-On Exercises

### **Exercise 1: File Management Automation**
- **Objective**: Create bash scripts to organize manufacturing data files
- **Data**: Various file formats (CSV, JSON, logs)
- **Deliverable**: Automated file organization script

### **Exercise 2: Scheduled Data Processing**
- **Objective**: Set up cronjobs for automated data processing
- **Data**: Manufacturing logs, quality reports, error messages
- **Deliverable**: Cronjob configuration and scheduled processing script

### **Exercise 3: Text Processing Pipeline**
- **Objective**: Build text processing pipeline for manufacturing logs
- **Data**: Manufacturing logs, quality reports, error messages
- **Deliverable**: Text processing and analysis script

### **Exercise 4: Python Data Processing**
- **Objective**: Create Python scripts for data preprocessing
- **Data**: Manufacturing datasets in various formats
- **Deliverable**: Data processing and cleaning pipeline

### **Exercise 5: SQL Data Analysis**
- **Objective**: Write SQL queries for manufacturing data analysis
- **Data**: Manufacturing database with multiple tables
- **Deliverable**: Complex SQL analysis queries

## Key Language Concepts

### **Bash & UNIX**
- **File System**: Directory structure and navigation
- **Text Processing**: grep, sed, awk for pattern matching
- **Pipelines**: Combining commands for complex operations
- **Scripting**: Automation and batch processing
- **Cronjobs**: Scheduled task automation

### **Python**
- **Data Structures**: Lists, dictionaries, sets, tuples
- **Control Flow**: Conditionals, loops, functions
- **Libraries**: pandas, numpy, requests, sqlite3
- **Error Handling**: Try-except blocks and logging

### **SQL**
- **Query Structure**: SELECT, FROM, WHERE, ORDER BY
- **Joins**: Combining data from multiple tables
- **Aggregations**: GROUP BY, aggregate functions
- **Performance**: Indexing and query optimization

### **Language Integration**
- **Shell Integration**: Python subprocess and os modules
- **Database Integration**: Python database connectors
- **Workflow Automation**: Combining multiple languages
- **Error Handling**: Cross-language error management
- **Scheduled Automation**: Cronjobs and task scheduling

## Assessment Criteria

### **Knowledge Checkpoints**
- [ ] Navigate file systems using UNIX commands
- [ ] Process text using grep, sed, and awk
- [ ] Write basic bash scripts for automation
- [ ] Set up and manage cronjobs for scheduled tasks
- [ ] Create Python scripts for data processing
- [ ] Write SQL queries for data extraction
- [ ] Integrate multiple languages in workflows

### **Project Milestones**
- **Milestone 1**: File management automation script
- **Milestone 2**: Scheduled data processing with cronjobs
- **Milestone 3**: Text processing pipeline
- **Milestone 4**: Python data processing workflow
- **Milestone 5**: SQL data analysis queries

## Success Metrics

### **Technical Competencies**
- [ ] UNIX command-line proficiency
- [ ] Bash scripting and automation
- [ ] Cronjob setup and management
- [ ] Python programming fundamentals
- [ ] SQL querying and database operations
- [ ] Language integration and workflows
- [ ] Error handling and debugging

### **Business Applications**
- [ ] Automated data processing pipelines
- [ ] Scheduled data collection and processing
- [ ] File organization and management
- [ ] Text analysis and log processing
- [ ] Database operations and reporting
- [ ] Cross-language workflow automation
- [ ] Reproducible data science processes

---

*This phase provides essential language and tool skills for data science, focusing on practical applications and workflow automation using real-world manufacturing data, including scheduled automation with cronjobs.* 