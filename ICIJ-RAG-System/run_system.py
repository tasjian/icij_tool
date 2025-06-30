#!/usr/bin/env python3
"""
ICIJ RAG System Launcher
Easy way to start different components of the system
"""

import subprocess
import sys
import os
import time
import signal
import threading

def load_env():
    """Load environment variables from .env file"""
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def run_enhanced_ui():
    """Run the enhanced investigation interface"""
    print("🕵️ Starting Enhanced ICIJ Investigation Interface...")
    print("📍 Will be available at: http://127.0.0.1:7865")
    print("🦊 Opens automatically in Firefox")
    subprocess.run([sys.executable, 'enhanced_icij_ui.py'])

def run_basic_ui():
    """Run the basic chat interface"""
    print("💬 Starting Basic ICIJ Chat Interface...")
    print("📍 Will be available at: http://127.0.0.1:7864")
    subprocess.run([sys.executable, 'icij_chat_interface.py'])

def run_server():
    """Run the API server only"""
    print("🚀 Starting ICIJ RAG API Server...")
    print("📍 Will be available at: http://127.0.0.1:9012")
    print("📖 API docs: http://127.0.0.1:9012/docs")
    subprocess.run([sys.executable, 'icij_server_app.py'])

def run_test():
    """Run system tests"""
    print("🧪 Running ICIJ RAG System Tests...")
    subprocess.run([sys.executable, 'test_icij_system.py'])

def run_full_system():
    """Run server and enhanced UI together"""
    print("🚀 Starting Full ICIJ RAG System...")
    
    # Start server in background
    print("📡 Starting API server...")
    server_process = subprocess.Popen([sys.executable, 'icij_server_app.py'])
    
    # Wait for server to start
    print("⏳ Waiting for server to initialize...")
    time.sleep(10)
    
    try:
        # Start enhanced UI
        print("🖥️  Starting enhanced interface...")
        subprocess.run([sys.executable, 'enhanced_icij_ui.py'])
    except KeyboardInterrupt:
        print("\n🛑 Stopping system...")
    finally:
        server_process.terminate()
        server_process.wait()

def show_menu():
    """Show the main menu"""
    print("\n🕵️ ICIJ RAG System Launcher")
    print("=" * 40)
    print("1. Enhanced Investigation Interface (Recommended)")
    print("2. Basic Chat Interface")
    print("3. API Server Only")
    print("4. Run System Tests")
    print("5. Full System (Server + Enhanced UI)")
    print("6. Exit")
    print("=" * 40)

def main():
    # Load environment
    load_env()
    
    # Check if NVIDIA API key is set
    if not os.environ.get('NVIDIA_API_KEY'):
        print("⚠️  NVIDIA API key not found!")
        print("Please run: python setup.py")
        sys.exit(1)
    
    while True:
        show_menu()
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            run_enhanced_ui()
        elif choice == '2':
            run_basic_ui()
        elif choice == '3':
            run_server()
        elif choice == '4':
            run_test()
        elif choice == '5':
            run_full_system()
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()