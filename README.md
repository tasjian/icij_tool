# 🕵️ ICIJ Offshore Leaks Investigation System

A complete **Graph-Enhanced RAG system** for investigating offshore financial data using the **ICIJ Offshore Leaks database**. This system combines **graph analysis** with **vector embeddings** and **interactive visualizations** to enable sophisticated financial investigations.

## 🚀 Quick Start

### 1. **Setup** (Run once)
```bash
python setup.py
```
This will:
- Install all required packages
- Prompt you to enter your NVIDIA API key
- Initialize the vector database

**Note:** You'll need an NVIDIA API key from https://build.nvidia.com/explore/discover

### 2. **Launch System**
```bash
python run_system.py
```
Choose from the menu:
- **Enhanced Investigation Interface** (Recommended) - With interactive visualizations
- **Basic Chat Interface**
- **API Server Only**
- **System Tests**

## 📊 Database Statistics (Real ICIJ Data)

- **🏢 814,617 Offshore Entities** - Companies, trusts, foundations from actual ICIJ leaks
- **👥 771,369 Officers/Individuals** - Directors, beneficial owners, shareholders  
- **🔗 3.3M+ Relationships** - Real network connections between entities and people
- **📍 402,321 Addresses** - Actual offshore financial centers and jurisdictions
- **📑 Multiple Investigations** - Panama Papers, Paradise Papers, Pandora Papers, Bahamas Leaks, etc.

## 🔍 Investigation Capabilities

### **Example Queries (Optimized for Visualizations)**
1. **"Show me offshore entities across Panama, British Virgin Islands, and Cayman Islands"**
2. **"Compare offshore structures revealed in Panama Papers versus Paradise Papers"**
3. **"Find all types of offshore entities including companies, trusts, and foundations"**
4. **"Analyze the complete offshore network including all major tax havens and investigation sources"**

### **Visualization Features**
- 🌍 **Jurisdiction Bar Charts** - Entities by geographic location
- 🏢 **Entity Type Distribution** - Companies, trusts, foundations breakdown
- 📰 **Investigation Sources** - Panama Papers, Paradise Papers, etc.
- 📊 **Summary Statistics** - Overview of investigation results
- 📈 **Interactive HTML/CSS Charts** - Professional styled visualizations

## 🛠️ System Architecture

### **Core Components**

#### **Enhanced UI with Visualizations**
- **`enhanced_icij_ui.py`** - Advanced Gradio interface with HTML/CSS charts
- **`icij_chat_interface.py`** - Basic chat interface
- **`run_system.py`** - Easy system launcher with menu

#### **Graph & Data Processing**
- **`graph_retriever.py`** - Graph-enhanced document retriever using NetworkX
- **`load_real_icij_data.py`** - Real ICIJ data loader from CSV files
- **`create_icij_vectorstore.py`** - Creates vector embeddings from graph data

#### **API Server**
- **`icij_server_app.py`** - LangServe server with offshore investigation endpoints

#### **Setup & Testing**
- **`setup.py`** - One-time system setup with dependency installation
- **`test_icij_system.py`** - Complete system testing
- **`requirements.txt`** - Python dependencies

### **Data Pipeline**
```
Real ICIJ CSV Files → Graph Construction → Vector Embeddings → RAG Pipeline → Interactive UI
```

1. **📁 Data Loading** - Real ICIJ CSV files processed by `RealICIJDataLoader`
2. **🕸️ Graph Construction** - NetworkX graph with entities, officers, addresses
3. **📊 Vector Embeddings** - FAISS vector store with document embeddings
4. **🔍 Hybrid Retrieval** - Combined graph traversal + semantic search
5. **📈 Visualization** - Interactive charts and data analysis
6. **🤖 AI Generation** - NVIDIA AI endpoints for response generation

## 🌐 Web Interfaces

- **Enhanced Interface:** http://127.0.0.1:7865 (With visualizations)
- **Basic Interface:** http://127.0.0.1:7864
- **API Documentation:** http://localhost:9012/docs

## 🛠️ API Endpoints

When running the server (`python icij_server_app.py`):

- **`/health`** - System health check and database statistics
- **`/stats`** - Detailed database analytics
- **`/retriever`** - Graph-enhanced document retrieval
- **`/generator`** - Investigation response generation
- **`/basic_chat`** - General LLM interaction

## 🧪 Testing

Run the complete system test:
```bash
python test_icij_system.py
```

This validates:
- ✅ Server health and connectivity
- ✅ Database statistics and data loading
- ✅ Document retrieval functionality
- ✅ Investigation response generation
- ✅ Graph-enhanced RAG pipeline

## 📋 Requirements

- **Python 3.8+**
- **NVIDIA API Key** (for embeddings and chat)
- **8GB+ RAM** (for vector store operations)
- **Web Browser** (for enhanced interface)

## 🔒 Security & Privacy

- **Real ICIJ Data:** Uses actual offshore leaks data from publicly released investigations
- **No Hardcoded Keys:** API keys managed through environment variables
- **Educational Purpose:** Designed for learning investigative techniques and journalism
- **Responsible Use:** Data should be used ethically for research and education only

## 🎓 Educational Value

This system demonstrates:
- **Graph Database Integration** with RAG systems
- **Financial Investigation** techniques using AI
- **Network Analysis** for relationship discovery
- **Data Visualization** for investigative insights
- **Multi-source Information** synthesis
- **Investigative Journalism** support tools

Perfect for learning about:
- Offshore financial structures and tax havens
- Graph-enhanced AI systems and retrieval
- Financial crime investigation techniques
- Data visualization and analysis
- AI-powered investigative tools

## 🗂️ File Structure

```
ICIJ-RAG-System/
├── enhanced_icij_ui.py          # Main UI with visualizations
├── icij_server_app.py           # API server
├── graph_retriever.py           # Graph-enhanced retrieval
├── load_real_icij_data.py       # Real data loading
├── setup.py                     # System setup
├── run_system.py               # System launcher
├── requirements.txt            # Dependencies
├── icij_data/                  # ICIJ CSV data files
├── icij_docstore_index.tgz     # Pre-built vector store
└── README.md                   # This file
```

## 🚨 Important Notes

### **Data Authenticity**
- All entities, officers, and relationships are from **real ICIJ public releases**
- Data includes actual names and connections from offshore investigations
- System loads performance-optimized subsets of the full dataset

### **Performance**
- System loads configurable subsets for optimal performance
- Full dataset contains millions of records
- Vector store optimized for investigation queries

### **Ethical Considerations**
- Data is from **public ICIJ investigations** available to researchers
- Should be used for **educational and research purposes**
- Respect privacy and use information responsibly

---

**🚀 Ready for sophisticated offshore financial investigations with AI-powered graph analysis and interactive visualizations!**