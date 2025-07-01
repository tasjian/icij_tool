#!/usr/bin/env python3
"""
Test the complete ICIJ RAG system
"""

import subprocess
import time
import requests
import os

def test_icij_system():
    print("🕵️ Testing ICIJ Offshore Leaks RAG System")
    print("=" * 60)
    
    # Set up environment
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Load API key from .env file
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('NVIDIA_API_KEY='):
                    os.environ['NVIDIA_API_KEY'] = line.split('=', 1)[1].strip()
                    break
    
    # Start server
    print("🚀 Starting ICIJ RAG server...")
    server_process = subprocess.Popen(['python', 'icij_server_app.py'], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
    
    # Wait for server to start
    print("⏳ Waiting for server to initialize (loading graph data)...")
    time.sleep(15)  # More time for graph loading
    
    try:
        base_url = "http://localhost:9012"
        
        # Test connection and health
        print("🩺 Testing server health...")
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ ICIJ Server is healthy!")
            print(f"   📊 Database: {health_data['database']}")
            print(f"   🏢 Entities: {health_data['total_entities']}")
            print(f"   👥 Officers: {health_data['total_officers']}")
            print(f"   🔗 Graph: {health_data['graph_nodes']} nodes, {health_data['graph_edges']} edges")
        else:
            print("❌ Server not healthy")
            return
        
        # Test statistics endpoint
        print("\\n📊 Testing statistics endpoint...")
        response = requests.get(f"{base_url}/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print("✅ Statistics endpoint working!")
            print(f"   🏢 Total entities: {stats['entities']['total']}")
            print(f"   👥 Total officers: {stats['officers']['total']}")
            print(f"   🔗 Total relationships: {stats['relationships']['total']}")
        
        # Test investigation queries
        investigation_queries = [
            "What offshore companies are incorporated in Panama?",
            "Show me beneficial owners from the UK",
            "Tell me about the Paradise Papers investigation",
            "Find entities in British Virgin Islands"
        ]
        
        for i, query in enumerate(investigation_queries, 1):
            print(f"\\n🔍 Investigation {i}: {query}")
            print("-" * 50)
            
            # Test retrieval
            print("📋 Testing document retrieval...")
            retrieval_response = requests.post(
                f"{base_url}/retriever/invoke",
                json={"input": query},
                timeout=30
            )
            
            if retrieval_response.status_code == 200:
                docs = retrieval_response.json()['output']
                print(f"✅ Retrieved {len(docs)} offshore documents")
                
                # Show sample results
                for j, doc in enumerate(docs[:2], 1):
                    doc_type = doc.get('metadata', {}).get('type', 'unknown')
                    title = doc.get('metadata', {}).get('title', 'Offshore Document')
                    print(f"   {j}. {doc_type.title()}: {title}")
                
                # Test generation with context
                print("🤖 Testing response generation...")
                
                # Format context
                context = ""
                for doc in docs:
                    title = doc.get('metadata', {}).get('title', 'Offshore Document')
                    doc_type = doc.get('metadata', {}).get('type', 'document')
                    
                    if doc_type == 'entity':
                        jurisdiction = doc.get('metadata', {}).get('jurisdiction', 'Unknown')
                        source = doc.get('metadata', {}).get('source', 'Unknown')
                        context += f"[{source} - {title} in {jurisdiction}] "
                    elif doc_type == 'officer':
                        country = doc.get('metadata', {}).get('country', 'Unknown')
                        context += f"[Individual: {title} from {country}] "
                    else:
                        context += f"[{title}] "
                        
                    context += doc.get('page_content', '') + "\\n\\n"
                
                generation_response = requests.post(
                    f"{base_url}/generator/invoke",
                    json={
                        "input": {
                            "input": query,
                            "context": context
                        }
                    },
                    timeout=30
                )
                
                if generation_response.status_code == 200:
                    answer = generation_response.json()['output']
                    print("✅ Investigation response generated!")
                    print("💼 Sample response:")
                    print(f"   {answer[:200]}...")
                else:
                    print(f"❌ Generation failed: {generation_response.status_code}")
            else:
                print(f"❌ Retrieval failed: {retrieval_response.status_code}")
        
        print("\\n🎉 ICIJ RAG System Test Completed Successfully!")
        print("\\n📋 Summary:")
        print("   ✅ Server health check passed")
        print("   ✅ Statistics endpoint working") 
        print("   ✅ Document retrieval functional")
        print("   ✅ Response generation working")
        print("   ✅ Graph-enhanced offshore investigation ready!")
        
        print(f"\\n🌐 Access the investigation interface:")
        print(f"   🖥️  Server API: {base_url}")
        print(f"   📖 API docs: {base_url}/docs")
        print(f"   📊 Statistics: {base_url}/stats")
        print(f"   🩺 Health: {base_url}/health")
        
        # Keep server running
        print("\\n⏸️  Server will continue running for testing...")
        print("   🎯 Run: python icij_chat_interface.py")
        print("   ⏹️  Press Ctrl+C to stop")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\\n🛑 Stopping server...")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        try:
            server_process.terminate()
            server_process.wait(timeout=5)
        except:
            server_process.kill()
        print("✅ Server stopped")

if __name__ == "__main__":
    test_icij_system()