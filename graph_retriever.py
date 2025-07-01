#!/usr/bin/env python3
"""
Graph-based retriever for ICIJ Offshore Leaks data using real CSV data
Uses NetworkX for graph operations and similarity search with actual ICIJ data
"""

import networkx as nx
import pandas as pd
import os
from typing import List, Dict, Any, Tuple
import re
from langchain.schema import Document
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_community.vectorstores import FAISS
import numpy as np
from load_real_icij_data import RealICIJDataLoader

class ICIJGraphRetriever:
    """Graph-based retriever for real ICIJ offshore leaks data"""
    
    def __init__(self, embedder=None, data_dir=None):
        """Initialize with real ICIJ data loader"""
        self.graph = nx.MultiDiGraph()
        self.embedder = embedder or NVIDIAEmbeddings(model="nvidia/nv-embed-v1", truncate="END")
        self.data_loader = RealICIJDataLoader(data_dir)
        
        # Data storage
        self.entities = {}
        self.officers = {}
        self.addresses = {}
        self.relationships = []
        self.document_store = None
        
        print("🏗️  Real ICIJ Graph Retriever initialized")
        
    def load_icij_data(self, entity_limit: int = 5000, officer_limit: int = 3000, 
                      address_limit: int = 2000, relationship_limit: int = 10000):
        """Load real ICIJ data from CSV files into graph structure"""
        print("\n🕵️ Loading Real ICIJ Data into Graph...")
        print("=" * 60)
        
        # Load data using the real data loader
        self.entities, self.officers, self.addresses, self.relationships = \
            self.data_loader.load_all_data(
                entity_limit=entity_limit,
                officer_limit=officer_limit, 
                address_limit=address_limit,
                relationship_limit=relationship_limit
            )
        
        # Build the graph structure
        self._build_graph()
        
        print(f"\n🔗 Graph Construction Complete:")
        print(f"   📊 Nodes: {self.graph.number_of_nodes():,}")
        print(f"   🔗 Edges: {self.graph.number_of_edges():,}")
    
    def _build_graph(self):
        """Build NetworkX graph from loaded data"""
        print("\n🏗️  Building graph structure...")
        
        # Add entity nodes
        for entity_id, entity in self.entities.items():
            self.graph.add_node(
                entity_id, 
                type='entity',
                name=entity['name'],
                jurisdiction=entity['jurisdiction'],
                company_type=entity['company_type'],
                status=entity['status'],
                source=entity['source'],
                countries=entity['countries']
            )
        
        # Add officer nodes  
        for officer_id, officer in self.officers.items():
            self.graph.add_node(
                officer_id,
                type='officer',
                name=officer['name'],
                countries=officer['countries'],
                source=officer['source']
            )
        
        # Add address nodes
        for address_id, address in self.addresses.items():
            self.graph.add_node(
                address_id,
                type='address', 
                address=address['address'],
                countries=address['countries'],
                source=address['source']
            )
        
        # Add relationships as edges
        edge_count = 0
        for rel in self.relationships:
            start_node = rel['start_node']
            end_node = rel['end_node']
            rel_type = rel['rel_type']
            
            # Only add edge if both nodes exist in graph
            if self.graph.has_node(start_node) and self.graph.has_node(end_node):
                self.graph.add_edge(
                    start_node,
                    end_node,
                    relationship=rel_type,
                    link=rel['link'],
                    status=rel['status'],
                    source=rel['source']
                )
                edge_count += 1
        
        print(f"   ✅ Added {edge_count:,} valid relationships")
    
    def build_vector_store(self, max_docs: int = 5000):
        """Create vector store from graph data using real entities"""
        print(f"\n📊 Building vector store from real ICIJ data...")
        
        documents = []
        doc_count = 0
        
        # Create documents from real entities
        for entity_id, entity in self.entities.items():
            if doc_count >= max_docs:
                break
                
            # Get connected nodes for context
            connected_info = self._get_entity_connections(entity_id)
            
            # Create rich document content
            content = self._create_entity_document(entity, connected_info)
            
            metadata = {
                'entity_id': entity_id,
                'name': entity['name'],
                'type': 'entity',
                'jurisdiction': entity['jurisdiction'],
                'company_type': entity['company_type'],
                'status': entity['status'],
                'source': entity['source'],
                'countries': entity['countries'],
                'title': f"Entity: {entity['name']}"
            }
            
            documents.append(Document(page_content=content, metadata=metadata))
            doc_count += 1
        
        # Create documents from officers
        for officer_id, officer in self.officers.items():
            if doc_count >= max_docs:
                break
                
            # Get connected entities
            connected_info = self._get_officer_connections(officer_id)
            
            # Create document content
            content = self._create_officer_document(officer, connected_info)
            
            metadata = {
                'officer_id': officer_id,
                'name': officer['name'],
                'type': 'officer',
                'countries': officer['countries'],
                'source': officer['source'],
                'title': f"Officer: {officer['name']}"
            }
            
            documents.append(Document(page_content=content, metadata=metadata))
            doc_count += 1
        
        # Create investigation summary documents
        investigation_docs = self._create_investigation_documents()
        documents.extend(investigation_docs[:100])  # Limit investigation docs
        
        print(f"   📄 Created {len(documents):,} documents")
        
        # Build FAISS vector store
        if documents:
            self.document_store = FAISS.from_documents(documents, self.embedder)
            print(f"   ✅ Vector store built with {len(documents):,} documents")
        else:
            print("   ❌ No documents to create vector store")
    
    def _get_entity_connections(self, entity_id: str) -> Dict:
        """Get connections for an entity"""
        connections = {
            'officers': [],
            'addresses': [], 
            'other_entities': []
        }
        
        if not self.graph.has_node(entity_id):
            return connections
        
        # Get all connected nodes
        for neighbor in self.graph.neighbors(entity_id):
            node_data = self.graph.nodes[neighbor]
            edge_data = self.graph.get_edge_data(entity_id, neighbor)
            
            # Extract relationship info
            rel_info = ""
            if edge_data:
                rel_data = list(edge_data.values())[0]  # Get first edge data
                rel_info = rel_data.get('relationship', '')
            
            if node_data.get('type') == 'officer':
                connections['officers'].append({
                    'name': node_data.get('name', ''),
                    'countries': node_data.get('countries', ''),
                    'relationship': rel_info
                })
            elif node_data.get('type') == 'address':
                connections['addresses'].append({
                    'address': node_data.get('address', ''),
                    'countries': node_data.get('countries', ''),
                    'relationship': rel_info
                })
            elif node_data.get('type') == 'entity':
                connections['other_entities'].append({
                    'name': node_data.get('name', ''),
                    'jurisdiction': node_data.get('jurisdiction', ''),
                    'relationship': rel_info
                })
        
        return connections
    
    def _get_officer_connections(self, officer_id: str) -> Dict:
        """Get connections for an officer"""
        connections = {'entities': []}
        
        if not self.graph.has_node(officer_id):
            return connections
        
        # Get connected entities
        for neighbor in self.graph.neighbors(officer_id):
            node_data = self.graph.nodes[neighbor]
            edge_data = self.graph.get_edge_data(officer_id, neighbor)
            
            # Extract relationship info
            rel_info = ""
            if edge_data:
                rel_data = list(edge_data.values())[0]
                rel_info = rel_data.get('relationship', '')
            
            if node_data.get('type') == 'entity':
                connections['entities'].append({
                    'name': node_data.get('name', ''),
                    'jurisdiction': node_data.get('jurisdiction', ''),
                    'relationship': rel_info
                })
        
        return connections
    
    def _create_entity_document(self, entity: Dict, connections: Dict) -> str:
        """Create rich document content for an entity"""
        content = f"Offshore Entity: {entity['name']}\n"
        content += f"Entity ID: {entity['entity_id']}\n"
        content += f"Jurisdiction: {entity['jurisdiction']}\n"
        
        if entity['company_type']:
            content += f"Type: {entity['company_type']}\n"
        
        content += f"Status: {entity['status']}\n"
        
        if entity['incorporation_date']:
            content += f"Incorporation Date: {entity['incorporation_date']}\n"
        
        if entity['address']:
            content += f"Address: {entity['address']}\n"
        
        content += f"Source: {entity['source']}\n"
        
        # Add connection information
        if connections['officers']:
            content += f"\nConnected Officers: "
            officer_info = []
            for officer in connections['officers'][:5]:  # Limit to 5
                rel = officer['relationship'] or 'connected_to'
                officer_info.append(f"{officer['name']} ({rel})")
            content += ", ".join(officer_info) + "\n"
        
        if connections['addresses']:
            content += f"\nRegistered Addresses: "
            addr_info = []
            for addr in connections['addresses'][:3]:  # Limit to 3
                rel = addr['relationship'] or 'registered_address'
                addr_info.append(f"{addr['address']} ({rel})")
            content += "; ".join(addr_info) + "\n"
        
        # Add investigative context
        content += f"\nDescription: This is an offshore entity from the {entity['source']} investigation"
        if entity['jurisdiction']:
            content += f" incorporated in {entity['jurisdiction']}"
        
        content += f". This entity was revealed in the {entity['source']} investigation"
        if entity['jurisdiction']:
            content += f" and is incorporated in {entity['jurisdiction']}"
        content += "."
        
        return content
    
    def _create_officer_document(self, officer: Dict, connections: Dict) -> str:
        """Create document content for an officer/individual"""
        content = f"Individual: {officer['name']}\n"
        content += f"Officer ID: {officer['officer_id']}\n"
        
        if officer['countries']:
            content += f"Country: {officer['countries']}\n"
        
        content += f"Source: {officer['source']}\n"
        
        # Add connected entities
        if connections['entities']:
            content += f"\nConnected Entities: "
            entity_info = []
            for entity in connections['entities'][:5]:  # Limit to 5
                rel = entity['relationship'] or 'officer_of'
                entity_info.append(f"{entity['name']} in {entity['jurisdiction']} ({rel})")
            content += ", ".join(entity_info) + "\n"
        
        content += f"\nDescription: {officer['name']} is an individual"
        if officer['countries']:
            content += f" from {officer['countries']}"
        content += f" who appears in the {officer['source']} investigation"
        
        if connections['entities']:
            content += f" with connections to {len(connections['entities'])} offshore entities"
        
        content += "."
        
        return content
    
    def _create_investigation_documents(self) -> List[Document]:
        """Create summary documents for different investigations"""
        documents = []
        
        # Analyze sources in the data
        source_stats = {}
        for entity in self.entities.values():
            source = entity['source']
            if source not in source_stats:
                source_stats[source] = {'entities': 0, 'jurisdictions': set()}
            source_stats[source]['entities'] += 1
            source_stats[source]['jurisdictions'].add(entity['jurisdiction'])
        
        # Create investigation summary documents
        for source, stats in source_stats.items():
            content = f"Investigation: {source}\n\n"
            content += f"The {source} investigation revealed {stats['entities']:,} offshore entities "
            content += f"across {len(stats['jurisdictions'])} jurisdictions.\n\n"
            
            # Top jurisdictions for this source
            source_jurisdictions = {}
            for entity in self.entities.values():
                if entity['source'] == source:
                    juris = entity['jurisdiction']
                    source_jurisdictions[juris] = source_jurisdictions.get(juris, 0) + 1
            
            content += "Key jurisdictions include: "
            top_jurisdictions = sorted(source_jurisdictions.items(), key=lambda x: x[1], reverse=True)[:5]
            content += ", ".join([f"{j} ({c} entities)" for j, c in top_jurisdictions])
            content += ".\n\n"
            
            content += f"This investigation exposed complex offshore structures and financial networks "
            content += f"involving entities, individuals, and intermediaries across multiple jurisdictions."
            
            metadata = {
                'type': 'investigation',
                'source': source,
                'title': f"Investigation: {source}",
                'entity_count': stats['entities']
            }
            
            documents.append(Document(page_content=content, metadata=metadata))
        
        return documents
    
    def retrieve(self, query: str, k: int = 4) -> List[Document]:
        """Retrieve relevant documents using hybrid graph + vector search"""
        if not self.document_store:
            print("⚠️ Vector store not built. Building now...")
            self.build_vector_store()
        
        if not self.document_store:
            print("❌ Could not build vector store")
            return []
        
        # First, get initial results from vector search
        vector_docs = self.document_store.similarity_search(query, k=k*2)
        
        # Enhance with graph context
        enhanced_docs = self._enhance_with_graph_context(vector_docs, query)
        
        # Return top k results
        return enhanced_docs[:k]
    
    def _enhance_with_graph_context(self, docs: List[Document], query: str) -> List[Document]:
        """Enhance documents with graph context"""
        enhanced_docs = []
        
        for doc in docs:
            enhanced_doc = Document(
                page_content=doc.page_content,
                metadata=doc.metadata.copy()
            )
            
            # Add graph connectivity info to metadata
            if doc.metadata.get('type') == 'entity':
                entity_id = doc.metadata.get('entity_id')
                if entity_id and self.graph.has_node(entity_id):
                    # Add network connectivity information
                    degree = self.graph.degree(entity_id)
                    enhanced_doc.metadata['network_degree'] = degree
                    
                    # Add neighbor information
                    neighbors = list(self.graph.neighbors(entity_id))[:5]
                    neighbor_info = []
                    for neighbor in neighbors:
                        node_data = self.graph.nodes[neighbor]
                        if node_data.get('type') == 'officer':
                            neighbor_info.append(f"Officer: {node_data.get('name', 'Unknown')}")
                        elif node_data.get('type') == 'address':
                            neighbor_info.append(f"Address: {node_data.get('countries', 'Unknown')}")
                    
                    enhanced_doc.metadata['connected_to'] = "; ".join(neighbor_info)
            
            enhanced_docs.append(enhanced_doc)
        
        return enhanced_docs

def test_real_graph_retriever():
    """Test the real graph retriever"""
    print("🧪 Testing Real ICIJ Graph Retriever")
    print("=" * 50)
    
    try:
        # Set environment for testing
        os.environ['NVIDIA_API_KEY'] = 'your-nvidia-api-key-here'
        
        # Initialize retriever
        retriever = ICIJGraphRetriever()
        
        # Load real data with smaller limits for testing
        retriever.load_icij_data(
            entity_limit=1000,
            officer_limit=500, 
            address_limit=300,
            relationship_limit=2000
        )
        
        # Build vector store
        retriever.build_vector_store(max_docs=500)
        
        # Test queries with real data
        test_queries = [
            "offshore companies in Samoa",
            "Panama Papers entities",
            "beneficial owners and directors", 
            "entities in tax havens"
        ]
        
        print(f"\n🔍 Testing retrieval with real data:")
        for query in test_queries:
            print(f"\n   Query: {query}")
            docs = retriever.retrieve(query, k=3)
            for i, doc in enumerate(docs, 1):
                title = doc.metadata.get('title', 'Document')
                doc_type = doc.metadata.get('type', 'unknown')
                source = doc.metadata.get('source', 'Unknown')
                print(f"   {i}. [{doc_type.upper()}] {title} (Source: {source})")
        
        print(f"\n✅ Real ICIJ Graph Retriever test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_real_graph_retriever()