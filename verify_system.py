#!/usr/bin/env python3
"""
Verify ICIJ RAG System Completeness
Check if all necessary files are present and can be imported
"""

import os
import sys

def check_files():
    """Check if all required files are present"""
    required_files = [
        'enhanced_icij_ui.py',
        'icij_chat_interface.py', 
        'icij_server_app.py',
        'graph_retriever.py',
        'create_icij_data.py',
        'create_icij_vectorstore.py',
        'test_icij_system.py',
        'icij_docstore_index.tgz',
        'requirements.txt',
        'setup.py',
        'run_system.py',
        'README.md',
        'ICIJ_README.md'
    ]
    
    print("🔍 Checking required files...")
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING")
            missing_files.append(file)
    
    return missing_files

def check_imports():
    """Check if key modules can be imported"""
    print("\n🔍 Checking Python imports...")
    
    try:
        import graph_retriever
        print("  ✅ graph_retriever.py")
    except ImportError as e:
        print(f"  ❌ graph_retriever.py - {e}")
        return False
    
    try:
        import create_icij_data
        print("  ✅ create_icij_data.py")
    except ImportError as e:
        print(f"  ❌ create_icij_data.py - {e}")
        return False
    
    return True

def check_vector_store():
    """Check if vector store archive exists and can be extracted"""
    print("\n🔍 Checking vector store...")
    
    if not os.path.exists('icij_docstore_index.tgz'):
        print("  ❌ icij_docstore_index.tgz not found")
        return False
    
    # Check if it's a valid tar.gz file
    import tarfile
    try:
        with tarfile.open('icij_docstore_index.tgz', 'r:gz') as tar:
            files = tar.getnames()
            print(f"  ✅ Vector store archive contains {len(files)} files")
            return True
    except Exception as e:
        print(f"  ❌ Vector store archive corrupted: {e}")
        return False

def main():
    print("🕵️ ICIJ RAG System Verification")
    print("=" * 50)
    
    # Check working directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"📍 Working directory: {script_dir}")
    
    # Check files
    missing_files = check_files()
    
    # Check imports
    imports_ok = check_imports()
    
    # Check vector store
    vector_store_ok = check_vector_store()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 VERIFICATION SUMMARY")
    print("=" * 50)
    
    if not missing_files and imports_ok and vector_store_ok:
        print("✅ ALL CHECKS PASSED")
        print("🚀 System is ready to run!")
        print("\nNext steps:")
        print("1. Run: python setup.py (if first time)")
        print("2. Run: python run_system.py")
        return True
    else:
        print("❌ VERIFICATION FAILED")
        if missing_files:
            print(f"Missing files: {', '.join(missing_files)}")
        if not imports_ok:
            print("Import errors detected")
        if not vector_store_ok:
            print("Vector store issues detected")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)