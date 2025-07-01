#!/usr/bin/env python3
"""
Script to replace the old graph_retriever.py with the real data version
"""

import shutil
import os

def replace_graph_retriever():
    """Replace the mock data graph retriever with real data version"""
    
    # Backup the original
    original_file = "/Users/zac/Desktop/ICIJ-RAG-System/graph_retriever.py"
    backup_file = "/Users/zac/Desktop/ICIJ-RAG-System/graph_retriever_mock_backup.py"
    real_file = "/Users/zac/Desktop/ICIJ-RAG-System/real_graph_retriever.py"
    
    print("🔄 Replacing graph retriever with real data version...")
    
    # Create backup of original
    if os.path.exists(original_file):
        shutil.copy2(original_file, backup_file)
        print(f"✅ Backed up original to: {backup_file}")
    
    # Replace with real version
    if os.path.exists(real_file):
        shutil.copy2(real_file, original_file)
        print(f"✅ Replaced with real data version")
        
        # Update the class name in the file
        with open(original_file, 'r') as f:
            content = f.read()
        
        # Replace class name
        content = content.replace('RealICIJGraphRetriever', 'ICIJGraphRetriever')
        content = content.replace('real_graph_retriever.py', 'graph_retriever.py')
        
        with open(original_file, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated class names and imports")
    else:
        print(f"❌ Real graph retriever file not found: {real_file}")
        return False
    
    return True

def update_server_imports():
    """Update server to handle real data loading"""
    server_file = "/Users/zac/Desktop/ICIJ-RAG-System/icij_server_app.py"
    
    print("\n🔄 Updating server to use real data...")
    
    # Read current server file
    with open(server_file, 'r') as f:
        content = f.read()
    
    # Update the data loading section
    old_loading = """# Create the graph retriever for enhanced functionality
graph_retriever = ICIJGraphRetriever(embedder)
graph_retriever.load_icij_data()"""
    
    new_loading = """# Create the graph retriever for enhanced functionality
graph_retriever = ICIJGraphRetriever(embedder)
# Load real ICIJ data with reasonable limits for server performance
graph_retriever.load_icij_data(
    entity_limit=10000,
    officer_limit=5000, 
    address_limit=3000,
    relationship_limit=15000
)"""
    
    content = content.replace(old_loading, new_loading)
    
    # Write updated content
    with open(server_file, 'w') as f:
        f.write(content)
    
    print("✅ Updated server data loading")

if __name__ == "__main__":
    print("🕵️ Switching ICIJ RAG System to Real Data")
    print("=" * 60)
    
    success = replace_graph_retriever()
    if success:
        update_server_imports()
        print("\n✅ Successfully switched to real ICIJ data!")
        print("\nThe system now uses:")
        print("  📊 Real offshore entities from CSV files")
        print("  👥 Real officers and individuals")
        print("  📍 Real addresses")
        print("  🔗 Real relationships") 
        print("  📰 Actual investigation sources (Panama Papers, etc.)")
        print("\nNext steps:")
        print("  1. Test with: python test_icij_system.py")
        print("  2. Run interface: python enhanced_icij_ui.py")
    else:
        print("\n❌ Failed to switch to real data")