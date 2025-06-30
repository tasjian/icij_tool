# 🕵️ ICIJ Offshore Leaks RAG System

## 🎯 Overview

This directory now contains a **Graph-Enhanced RAG system** for investigating offshore financial data, replacing the academic papers with the **ICIJ Offshore Leaks database**. The system combines **Neo4j graph concepts** with **vector embeddings** to enable sophisticated financial investigations.

## 📊 Database Structure

### **ICIJ Offshore Leaks Data (Mock)**
- **🏢 500 Offshore Entities** - Companies, trusts, foundations
- **👥 300 Officers/Individuals** - Directors, beneficial owners, shareholders  
- **🔗 800 Relationships** - Connections between entities and officers
- **📍 200 Addresses** - Offshore financial centers
- **📑 5 Major Investigations** - Panama Papers, Paradise Papers, Pandora Papers, etc.

### **Graph Structure**
```
[Entity] --[officer_of]--> [Officer]
[Entity] --[located_at]--> [Address]
[Officer] --[director_of]--> [Entity]
[Officer] --[beneficial_owner]--> [Entity]
```

## 🛠️ Key Components

### **Core Files**

#### **Graph & Data Processing**
- **`create_icij_data.py`** - Generates mock ICIJ offshore leaks data
- **`graph_retriever.py`** - Graph-enhanced document retriever using NetworkX
- **`create_icij_vectorstore.py`** - Creates vector embeddings from graph data

#### **RAG Server**
- **`icij_server_app.py`** - LangServe server with offshore investigation endpoints
- **`icij_chat_interface.py`** - Specialized Gradio interface for financial investigations

#### **Testing & Utilities**
- **`test_icij_system.py`** - Complete system testing
- **`icij_docstore_index.tgz`** - Pre-built vector store with 805 offshore documents

## 🚀 Quick Start

### **Option 1: Run Investigation Interface**
```bash
python icij_chat_interface.py
```
**Available at:** http://localhost:7864

### **Option 2: Start API Server**
```bash
python icij_server_app.py
```
**Available at:** http://localhost:9012

### **Option 3: Run System Test**
```bash
python test_icij_system.py
```

## 🔍 Investigation Capabilities

### **Sample Queries**

#### **Entity Investigations**
- "What offshore companies are incorporated in Panama?"
- "Show me entities in the British Virgin Islands"
- "Find shell companies in the Cayman Islands"

#### **People & Relationships**
- "Show me beneficial owners from the UK"
- "Find directors and shareholders connected to offshore entities"
- "What individuals appear in multiple investigations?"

#### **Investigation Analysis**
- "What was revealed in the Paradise Papers?"
- "Compare findings from Panama Papers vs Pandora Papers"
- "Which jurisdictions appear most frequently?"

#### **Network Analysis**
- "Show me the network around [entity name]"
- "Find connections between [person] and offshore entities"
- "What are the most connected entities in the database?"

## 🛠️ API Endpoints

### **LangServe Endpoints (Port 9012)**

#### **`/basic_chat`**
- **Purpose:** General LLM interaction
- **Input:** `{"input": "your message"}`

#### **`/retriever`** 
- **Purpose:** Graph-enhanced offshore document retrieval
- **Input:** `{"input": "investigation query"}`
- **Output:** Offshore entities, officers, and relationships

#### **`/generator`**
- **Purpose:** Investigation-focused response generation
- **Input:** `{"input": {"input": "question", "context": "offshore data"}}`
- **Output:** Investigative analysis with citations

#### **`/health`**
- **Purpose:** System health and database statistics
- **Output:** Entity counts, graph metrics, system status

#### **`/stats`**
- **Purpose:** Detailed database statistics
- **Output:** Jurisdictions, entity types, investigations breakdown

## 📈 Technical Architecture

### **Graph-Enhanced RAG Pipeline**

1. **🔍 Query Processing**
   - Natural language investigation queries
   - Entity/person name extraction
   - Jurisdiction and relationship identification

2. **🕸️ Graph Retrieval**
   - NetworkX graph traversal
   - Multi-hop relationship exploration
   - Network analysis and pattern detection

3. **📊 Vector Search**
   - Semantic similarity search
   - Document embedding retrieval
   - Context-aware ranking

4. **🔗 Hybrid Enhancement**
   - Combine graph context with vector results
   - Relationship-enriched documents
   - Network connectivity information

5. **🎯 Investigation Response**
   - Financial investigation language
   - Jurisdiction-specific analysis
   - Source attribution (Panama Papers, etc.)

### **Performance Optimizations**

- **Pre-computed Graph:** NetworkX graph loaded at startup
- **Cached Embeddings:** FAISS vector store with 805 documents
- **Relationship Indexing:** Fast neighbor lookup for entities
- **Metadata Enrichment:** Source, jurisdiction, and type filtering

## 🧪 Testing Results

**Graph Database:**
- ✅ 1000 nodes (entities + officers + addresses)
- ✅ 800 relationships (director_of, beneficial_owner, etc.)
- ✅ Multi-hop traversal working
- ✅ Network analysis functional

**Vector Retrieval:**
- ✅ 805 documents created from graph data
- ✅ Entity-specific document formatting
- ✅ Investigation-specific document types
- ✅ Semantic search working

**RAG Pipeline:**
- ✅ Query understanding for offshore terms
- ✅ Graph-enhanced context retrieval
- ✅ Investigation-focused response generation
- ✅ Source attribution and citations

## 🌍 Investigative Features

### **Financial Intelligence**
- **Jurisdiction Analysis:** Tax haven identification and patterns
- **Entity Type Classification:** Companies, trusts, foundations
- **Relationship Mapping:** Director/beneficial owner networks
- **Investigation Correlation:** Cross-reference multiple data sources

### **Graph Analytics**
- **Network Centrality:** Most connected entities and individuals
- **Path Analysis:** Relationship chains between entities
- **Community Detection:** Clusters of related offshore structures
- **Temporal Analysis:** Incorporation dates and relationship timelines

### **Compliance Support**
- **Due Diligence:** Entity verification and background checks
- **Risk Assessment:** Connection analysis for compliance
- **Source Verification:** Investigation provenance tracking
- **Regulatory Reporting:** Structured data for authorities

## 🔒 Security & Privacy

- **Mock Data Only:** Uses simulated ICIJ-style data for demonstration
- **No Real PII:** All names, entities, and relationships are fictional
- **Educational Purpose:** Designed for learning investigative techniques
- **Privacy Compliant:** No actual offshore leaks data included

## 🎓 Educational Value

This system demonstrates:
- **Graph Database Integration** with RAG systems
- **Financial Investigation** techniques using AI
- **Network Analysis** for relationship discovery
- **Multi-source Information** synthesis
- **Investigative Journalism** support tools

Perfect for learning about:
- **Offshore financial structures**
- **Investigative data analysis** 
- **Graph-enhanced AI systems**
- **Financial crime investigation**
- **International journalism techniques**

---

**🚀 Ready for sophisticated offshore financial investigations with AI-powered graph analysis!**