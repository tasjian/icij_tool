# 🕵️ ICIJ RAG System - Standalone Package

A complete **Graph-Enhanced RAG system** for investigating offshore financial data using the **ICIJ Offshore Leaks database**. This system combines **Neo4j graph concepts** with **vector embeddings** to enable sophisticated financial investigations.

## 🚀 Quick Start

### 1. **Setup** (Run once)
```bash
python setup.py
```
This will:
- Install all required packages
- Set up your NVIDIA API key
- Initialize the vector database

### 2. **Launch System**
```bash
python run_system.py
```
Choose from the menu:
- **Enhanced Investigation Interface** (Recommended)
- **Basic Chat Interface**
- **API Server Only**
- **System Tests**

## 📊 What's Included

### **Core System Files**
- **`enhanced_icij_ui.py`** - Advanced Gradio investigation interface
- **`icij_chat_interface.py`** - Basic chat interface
- **`icij_server_app.py`** - LangServe API server
- **`graph_retriever.py`** - Graph-enhanced document retriever
- **`create_icij_data.py`** - Mock ICIJ data generator
- **`test_icij_system.py`** - Complete system testing

### **Setup & Management**
- **`setup.py`** - One-time system setup
- **`run_system.py`** - Easy system launcher
- **`requirements.txt`** - Python dependencies
- **`icij_docstore_index.tgz`** - Pre-built vector store (805 documents)

### **Documentation**
- **`ICIJ_README.md`** - Detailed technical documentation
- **`README.md`** - This file

## 🔍 Investigation Capabilities

### **Sample Queries**
- "What offshore companies are incorporated in Panama?"
- "Show me beneficial owners from the UK"
- "Find entities in the British Virgin Islands"
- "What was revealed in the Paradise Papers?"
- "Show me the network around [entity name]"

### **Database Statistics**
- **🏢 500 Offshore Entities** - Companies, trusts, foundations
- **👥 300 Officers/Individuals** - Directors, beneficial owners
- **🔗 800 Relationships** - Network connections
- **📍 200 Addresses** - Offshore financial centers
- **📑 5 Major Investigations** - Panama Papers, Paradise Papers, etc.

## 🛠️ API Endpoints

When running the server (`python icij_server_app.py`):

- **http://localhost:9012/docs** - API documentation
- **http://localhost:9012/health** - System health check
- **http://localhost:9012/stats** - Database statistics
- **http://localhost:9012/retriever** - Document retrieval
- **http://localhost:9012/generator** - Investigation response generation

## 🌐 Web Interfaces

- **Enhanced Interface:** http://127.0.0.1:7865 (Auto-opens in Firefox)
- **Basic Interface:** http://127.0.0.1:7864

## 🧪 Testing

Run the complete system test:
```bash
python test_icij_system.py
```

This validates:
- ✅ Server health and connectivity
- ✅ Database statistics
- ✅ Document retrieval functionality
- ✅ Investigation response generation
- ✅ Graph-enhanced RAG pipeline

## 🔒 Security & Privacy

- **Mock Data Only:** Uses simulated ICIJ-style data
- **No Real PII:** All names and entities are fictional
- **Educational Purpose:** Designed for learning investigative techniques
- **Privacy Compliant:** No actual offshore leaks data

## 📋 Requirements

- **Python 3.8+**
- **NVIDIA API Key** (for embeddings and chat)
- **8GB+ RAM** (for vector store operations)
- **Firefox Browser** (for enhanced interface)

## 🎓 Educational Value

This system demonstrates:
- **Graph Database Integration** with RAG systems
- **Financial Investigation** techniques using AI
- **Network Analysis** for relationship discovery
- **Multi-source Information** synthesis
- **Investigative Journalism** support tools

Perfect for learning about offshore financial structures, investigative data analysis, graph-enhanced AI systems, and financial crime investigation techniques.

---

**🚀 Ready for sophisticated offshore financial investigations with AI-powered graph analysis!**
