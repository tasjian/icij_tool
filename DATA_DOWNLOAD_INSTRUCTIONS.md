# 📁 Data Download Instructions

Due to GitHub's file size limitations, the large ICIJ data files are not included in this repository. Follow these instructions to set up the complete system.

## 🔍 Required Data Files

### **ICIJ Offshore Leaks Database**
Download the ICIJ Offshore Leaks database from the official ICIJ website:

**Source:** https://offshoreleaks.icij.org/pages/database

### **Required Files Structure**
```
ICIJ-RAG-System/
├── icij_data/
│   ├── nodes-entities.csv      # 189 MB - Offshore entities
│   ├── nodes-officers.csv      # 87 MB - Officers and individuals  
│   ├── nodes-addresses.csv     # 69 MB - Address information
│   ├── relationships.csv       # 247 MB - Entity relationships
│   ├── nodes-intermediaries.csv
│   └── nodes-others.csv
└── icij-offshoreleaks-5.13.0.dump  # 348 MB - Full database dump
```

## 🚀 Quick Setup

### **Option 1: Automatic Setup (Recommended)**
```bash
python setup.py
```
The setup script will:
1. Check for required data files
2. Provide download instructions if missing
3. Create the vector store automatically

### **Option 2: Manual Download**
1. **Visit**: https://offshoreleaks.icij.org/pages/database
2. **Download**: The CSV files or database dump
3. **Extract**: Place files in the correct directories as shown above
4. **Run**: `python setup.py` to initialize the system

## 📊 Data Statistics

Once downloaded, you'll have access to:
- **🏢 814,617 Offshore Entities** - Real company and trust data
- **👥 771,369 Officers/Individuals** - Directors and beneficial owners
- **🔗 3.3M+ Relationships** - Network connections
- **📍 402,321 Addresses** - Offshore financial centers
- **📑 Multiple Investigations** - Panama Papers, Paradise Papers, etc.

## ⚠️ Important Notes

### **Data Authenticity**
- All data is from **real ICIJ public investigations**
- Contains **actual names and entities** from offshore leaks
- Use **responsibly** for educational and research purposes

### **File Sizes**
- Total download size: ~1GB
- Ensure adequate disk space
- Processing requires 8GB+ RAM

### **Legal Considerations**
- Data is **publicly available** from ICIJ
- Use for **educational/research purposes**
- Respect privacy and ethical guidelines

## 🔗 Alternative Data Sources

If ICIJ data is unavailable, the system includes:
- **Mock data generator** (`create_icij_data.py`)
- **Smaller sample datasets** for testing
- **Development mode** with reduced data requirements

## 🛠️ Troubleshooting

### **Download Issues**
```bash
# Check if data directory exists
ls -la icij_data/

# Verify file sizes
du -h icij_data/*.csv

# Test data loading
python test_icij_system.py
```

### **Setup Problems**
- Ensure Python 3.8+ is installed
- Check available disk space (>2GB recommended)
- Verify NVIDIA API key configuration

---

**📞 Need Help?** Check the main README.md for complete setup instructions and troubleshooting.