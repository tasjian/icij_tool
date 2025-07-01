#!/usr/bin/env python3
"""
Create vector store from ICIJ graph data
"""

import os
from graph_retriever import ICIJGraphRetriever
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings

def create_icij_vectorstore():
    """Create and save ICIJ vector store"""
    
    # Set up environment
    os.environ['NVIDIA_API_KEY'] = 'your-nvidia-api-key-here'
    
    print("🏗️  Creating ICIJ vector store...")
    
    # Initialize retriever
    embedder = NVIDIAEmbeddings(model="nvidia/nv-embed-v1", truncate="END")
    retriever = ICIJGraphRetriever(embedder)
    
    # Load ICIJ data and build vector store
    retriever.load_icij_data()
    retriever.build_vector_store()
    
    # Save the vector store
    print("💾 Saving vector store...")
    retriever.document_store.save_local("icij_docstore_index")
    
    # Create compressed version
    import subprocess
    subprocess.run(['tar', 'czvf', 'icij_docstore_index.tgz', 'icij_docstore_index'])
    
    # Clean up directory
    import shutil
    shutil.rmtree('icij_docstore_index')
    
    print("✅ ICIJ vector store created and saved!")
    
    # Test the vector store
    print("\n🧪 Testing retrieval...")
    test_queries = [
        "offshore companies in Panama",
        "beneficial owners and directors", 
        "Paradise Papers investigation",
        "entities in British Virgin Islands"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        docs = retriever.retrieve(query, k=2)
        for i, doc in enumerate(docs, 1):
            title = doc.metadata.get('title', 'Document')
            print(f"  {i}. {title}")
            print(f"     {doc.page_content[:150]}...")

if __name__ == "__main__":
    # Set working directory to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    create_icij_vectorstore()