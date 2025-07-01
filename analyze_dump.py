#!/usr/bin/env python3
"""
Analyze the ICIJ Offshore Leaks dump file
Try different approaches to understand the file format and extract data
"""

import os
import struct
import gzip
import bz2
import lzma
import sqlite3
import json

def analyze_dump_file(filepath):
    """Analyze the dump file to understand its format"""
    print(f"Analyzing file: {filepath}")
    
    # Check file size
    size = os.path.getsize(filepath)
    print(f"File size: {size:,} bytes ({size/1024/1024:.1f} MB)")
    
    # Read first few bytes to check magic numbers
    with open(filepath, 'rb') as f:
        header = f.read(100)
        print(f"First 20 bytes (hex): {header[:20].hex()}")
        print(f"First 20 bytes (ascii): {header[:20]}")
    
    # Try different decompression methods
    compression_methods = [
        ("gzip", gzip.open),
        ("bz2", bz2.open),
        ("lzma", lzma.open)
    ]
    
    for method_name, open_func in compression_methods:
        try:
            with open_func(filepath, 'rt', encoding='utf-8', errors='ignore') as f:
                content = f.read(1000)
                if content and len(content) > 10:
                    print(f"\n✅ Successfully decompressed with {method_name}:")
                    print(f"Sample content: {content[:200]}...")
                    return method_name, content
        except Exception as e:
            print(f"❌ {method_name} decompression failed: {e}")
    
    # Try reading as binary and look for patterns
    try:
        with open(filepath, 'rb') as f:
            # Look for common database signatures
            f.seek(0)
            chunk = f.read(1024 * 1024)  # Read 1MB
            
            # Look for CSV-like patterns
            if b',' in chunk and b'\n' in chunk:
                print("\n📊 Found comma-separated patterns - might be CSV data")
            
            # Look for JSON patterns
            if b'{' in chunk and b'}' in chunk:
                print("\n📊 Found JSON-like patterns")
            
            # Look for SQL patterns
            sql_keywords = [b'CREATE', b'INSERT', b'TABLE', b'SELECT']
            for keyword in sql_keywords:
                if keyword in chunk:
                    print(f"\n📊 Found SQL keyword: {keyword.decode()}")
            
            # Look for Neo4j patterns
            neo4j_keywords = [b'Node', b'Relationship', b'MATCH', b'CREATE']
            for keyword in neo4j_keywords:
                if keyword in chunk:
                    print(f"\n📊 Found Neo4j-like keyword: {keyword.decode()}")
                    
    except Exception as e:
        print(f"❌ Binary analysis failed: {e}")
    
    return None, None

def try_as_sqlite(filepath):
    """Try to open as SQLite database"""
    try:
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if tables:
            print(f"\n✅ SQLite database found with tables: {tables}")
            return True
        conn.close()
    except Exception as e:
        print(f"❌ Not a SQLite database: {e}")
    return False

def search_for_csv_files():
    """Search for any CSV files that might contain ICIJ data"""
    print("\n🔍 Searching for CSV files in directory...")
    base_dir = "/Users/zac/Desktop/ICIJ-RAG-System"
    
    for file in os.listdir(base_dir):
        if file.endswith('.csv'):
            filepath = os.path.join(base_dir, file)
            print(f"Found CSV: {file}")
            
            # Analyze CSV structure
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    header = f.readline().strip()
                    sample_line = f.readline().strip()
                    print(f"  Header: {header}")
                    print(f"  Sample: {sample_line}")
            except Exception as e:
                print(f"  Error reading CSV: {e}")

def main():
    filepath = "/Users/zac/Desktop/ICIJ-RAG-System/icij-offshoreleaks-5.13.0.dump"
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return
    
    # Analyze the dump file
    compression_type, sample_content = analyze_dump_file(filepath)
    
    # Try as SQLite
    try_as_sqlite(filepath)
    
    # Search for CSV files
    search_for_csv_files()
    
    # If we found compressed content, save a sample
    if sample_content:
        sample_file = "/Users/zac/Desktop/ICIJ-RAG-System/dump_sample.txt"
        with open(sample_file, 'w') as f:
            f.write(sample_content[:5000])  # Save first 5KB
        print(f"\n💾 Saved sample content to: {sample_file}")

if __name__ == "__main__":
    main()