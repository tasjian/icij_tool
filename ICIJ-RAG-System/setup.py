#!/usr/bin/env python3
"""
ICIJ RAG System Setup Script
Initializes the system and creates the necessary data and vector store
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

def setup_environment():
    """Set up environment variables"""
    print("🔧 Setting up environment...")
    nvidia_key = input("Enter your NVIDIA API key: ").strip()
    
    # Create .env file
    with open('.env', 'w') as f:
        f.write(f"NVIDIA_API_KEY={nvidia_key}\n")
    
    # Also set in current session
    os.environ['NVIDIA_API_KEY'] = nvidia_key
    print("✅ Environment configured!")

def initialize_data():
    """Initialize ICIJ mock data and vector store"""
    print("🏗️ Creating ICIJ mock data...")
    subprocess.check_call([sys.executable, 'create_icij_data.py'])
    
    print("📊 Creating vector store...")
    subprocess.check_call([sys.executable, 'create_icij_vectorstore.py'])

def extract_vector_store():
    """Extract pre-built vector store"""
    print("📂 Extracting vector store...")
    subprocess.check_call(['tar', 'xzf', 'icij_docstore_index.tgz'])

def main():
    print("🕵️ ICIJ RAG System Setup")
    print("=" * 50)
    
    try:
        # Install requirements
        install_requirements()
        
        # Setup environment
        setup_environment()
        
        # Extract vector store (faster than rebuilding)
        extract_vector_store()
        
        print("\n✅ Setup completed successfully!")
        print("\n🚀 You can now run:")
        print("   python enhanced_icij_ui.py      # Enhanced investigation interface")
        print("   python icij_chat_interface.py   # Basic chat interface")
        print("   python test_icij_system.py      # System test")
        print("   python icij_server_app.py       # API server only")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()