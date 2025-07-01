#!/usr/bin/env python3
"""
Create vector store from real ICIJ data instead of mock data
"""

import os
from graph_retriever import ICIJGraphRetriever
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings

def create_real_icij_vectorstore():
    """Create and save ICIJ vector store using real data"""
    
    # Set up environment - load from .env file if exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_file = os.path.join(script_dir, '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('NVIDIA_API_KEY='):
                    os.environ['NVIDIA_API_KEY'] = line.split('=', 1)[1].strip()
                    break
    else:
        # Use placeholder for now
        os.environ['NVIDIA_API_KEY'] = 'your-nvidia-api-key-here'
    
    print("🏗️  Creating Real ICIJ Vector Store...")
    print("=" * 60)
    
    try:
        # Initialize retriever with real data
        embedder = NVIDIAEmbeddings(model="nvidia/nv-embed-v1", truncate="END")
        retriever = ICIJGraphRetriever(embedder)
        
        # Load real ICIJ data with reasonable limits for vector store
        retriever.load_icij_data(
            entity_limit=5000,    # 5K entities
            officer_limit=3000,   # 3K officers  
            address_limit=2000,   # 2K addresses
            relationship_limit=10000  # 10K relationships
        )
        
        # Build vector store from real data
        print("\n📊 Building vector store from real ICIJ data...")
        retriever.build_vector_store(max_docs=3000)  # Create 3000 documents
        
        if retriever.document_store:
            # Save the vector store
            print("💾 Saving vector store...")
            retriever.document_store.save_local("real_icij_docstore_index")
            
            # Create compressed version
            import subprocess
            print("📦 Creating compressed archive...")
            subprocess.run(['tar', 'czf', 'real_icij_docstore_index.tgz', 'real_icij_docstore_index'])
            
            # Clean up directory
            import shutil
            shutil.rmtree('real_icij_docstore_index')
            
            print("✅ Real ICIJ vector store created and saved!")
            
            # Test the vector store by loading it back
            print("\n🧪 Testing the saved vector store...")
            test_retrieval()
            
        else:
            print("❌ Failed to create vector store")
            return False
    
    except Exception as e:
        print(f"❌ Error creating vector store: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_retrieval():
    """Test retrieval with real data"""
    try:
        # Extract and test the vector store
        import subprocess
        subprocess.run(['tar', 'xzf', 'real_icij_docstore_index.tgz'])
        
        # Create retriever and load the vector store
        embedder = NVIDIAEmbeddings(model="nvidia/nv-embed-v1", truncate="END")
        retriever = ICIJGraphRetriever(embedder)
        
        # Load a small amount of data for graph context
        retriever.load_icij_data(
            entity_limit=1000,
            officer_limit=500,
            address_limit=300,
            relationship_limit=2000
        )
        
        # Load the saved vector store
        from langchain_community.vectorstores import FAISS
        retriever.document_store = FAISS.load_local("real_icij_docstore_index", embedder, 
                                                   allow_dangerous_deserialization=True)
        
        # Test queries with real data
        test_queries = [
            "offshore companies in Samoa",
            "Panama Papers investigation", 
            "beneficial owners from China",
            "entities in tax havens"
        ]
        
        print(f"🔍 Testing retrieval with real ICIJ data:")
        for query in test_queries:
            print(f"\n   Query: {query}")
            docs = retriever.retrieve(query, k=3)
            
            if docs:
                for i, doc in enumerate(docs, 1):
                    title = doc.metadata.get('title', 'Document')
                    doc_type = doc.metadata.get('type', 'unknown')
                    source = doc.metadata.get('source', 'Unknown')
                    jurisdiction = doc.metadata.get('jurisdiction', '')
                    print(f"   {i}. [{doc_type.upper()}] {title}")
                    if jurisdiction:
                        print(f"      Jurisdiction: {jurisdiction}, Source: {source}")
                    else:
                        print(f"      Source: {source}")
            else:
                print("   No results found")
        
        # Clean up test directory
        import shutil
        shutil.rmtree('real_icij_docstore_index')
        
        print(f"\n✅ Vector store test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def replace_old_vectorstore():
    """Replace the old mock vector store with the real one"""
    print("\n🔄 Replacing old vector store with real data version...")
    
    import shutil
    
    # Backup old vector store
    if os.path.exists('icij_docstore_index.tgz'):
        shutil.copy2('icij_docstore_index.tgz', 'icij_docstore_index_mock_backup.tgz')
        print("✅ Backed up old vector store")
    
    # Replace with real version
    if os.path.exists('real_icij_docstore_index.tgz'):
        shutil.copy2('real_icij_docstore_index.tgz', 'icij_docstore_index.tgz')
        print("✅ Replaced with real data vector store")
        return True
    else:
        print("❌ Real vector store not found")
        return False

if __name__ == "__main__":
    print("🕵️ Creating Real ICIJ Vector Store")
    print("=" * 60)
    
    # Set working directory to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    success = create_real_icij_vectorstore()
    
    if success:
        replace_old_vectorstore()
        print("\n🎉 Successfully created real ICIJ vector store!")
        print("\nThe system now uses:")
        print("  📊 Real offshore entities from ICIJ CSV data")
        print("  👥 Real officers and beneficial owners")
        print("  📍 Real addresses and jurisdictions")
        print("  📰 Actual investigation sources (Panama Papers)")
        print("  🔗 Real entity-officer-address relationships")
        print("\nVector store contains:")
        print("  📄 Documents created from real ICIJ data")
        print("  🔍 Searchable offshore entity information")
        print("  🕸️  Graph-enhanced context for investigations")
    else:
        print("\n❌ Failed to create real ICIJ vector store")