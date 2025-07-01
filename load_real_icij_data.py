#!/usr/bin/env python3
"""
Load real ICIJ Offshore Leaks data from CSV files
Replaces the mock data generation with actual ICIJ data
"""

import pandas as pd
import os
from typing import Dict, List, Tuple
import csv

class RealICIJDataLoader:
    """Load and process real ICIJ offshore leaks data from CSV files"""
    
    def __init__(self, data_dir: str = None):
        """Initialize the data loader"""
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), 'icij_data')
        self.data_dir = data_dir
        
        # Verify data directory exists
        if not os.path.exists(data_dir):
            raise FileNotFoundError(f"ICIJ data directory not found: {data_dir}")
        
        self.entities = {}
        self.officers = {}
        self.addresses = {}
        self.intermediaries = {}
        self.others = {}
        self.relationships = []
        
        print(f"🏗️  Real ICIJ Data Loader initialized")
        print(f"📁 Data directory: {data_dir}")
    
    def load_entities(self, limit: int = None) -> Dict:
        """Load offshore entities from CSV"""
        entities_file = os.path.join(self.data_dir, 'nodes-entities.csv')
        print(f"📊 Loading entities from {entities_file}")
        
        entities = {}
        try:
            with open(entities_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    if limit and count >= limit:
                        break
                    
                    entity_id = row['node_id']
                    entity = {
                        'entity_id': entity_id,
                        'name': row['name'] or 'Unknown Entity',
                        'original_name': row['original_name'] or row['name'] or 'Unknown Entity',
                        'former_name': row['former_name'] or '',
                        'jurisdiction': row['jurisdiction'] or 'Unknown',
                        'jurisdiction_description': row['jurisdiction_description'] or '',
                        'company_type': row['company_type'] or 'Unknown',
                        'address': row['address'] or '',
                        'internal_id': row['internal_id'] or '',
                        'incorporation_date': row['incorporation_date'] or '',
                        'inactivation_date': row['inactivation_date'] or '',
                        'struck_off_date': row['struck_off_date'] or '',
                        'status': row['status'] or 'Unknown',
                        'service_provider': row['service_provider'] or 'Unknown',
                        'country_codes': row['country_codes'] or '',
                        'countries': row['countries'] or '',
                        'source': row['sourceID'] or 'Unknown',
                        'valid_until': row['valid_until'] or '',
                        'note': row['note'] or ''
                    }
                    entities[entity_id] = entity
                    count += 1
            
            print(f"✅ Loaded {len(entities):,} entities")
            return entities
            
        except Exception as e:
            print(f"❌ Error loading entities: {e}")
            return {}
    
    def load_officers(self, limit: int = None) -> Dict:
        """Load officers/individuals from CSV"""
        officers_file = os.path.join(self.data_dir, 'nodes-officers.csv')
        print(f"👥 Loading officers from {officers_file}")
        
        officers = {}
        try:
            with open(officers_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    if limit and count >= limit:
                        break
                    
                    officer_id = row['node_id']
                    officer = {
                        'officer_id': officer_id,
                        'name': row['name'] or 'Unknown Person',
                        'countries': row['countries'] or 'Unknown',
                        'country_codes': row['country_codes'] or '',
                        'source': row['sourceID'] or 'Unknown',
                        'valid_until': row['valid_until'] or '',
                        'note': row['note'] or ''
                    }
                    officers[officer_id] = officer
                    count += 1
            
            print(f"✅ Loaded {len(officers):,} officers")
            return officers
            
        except Exception as e:
            print(f"❌ Error loading officers: {e}")
            return {}
    
    def load_addresses(self, limit: int = None) -> Dict:
        """Load addresses from CSV"""
        addresses_file = os.path.join(self.data_dir, 'nodes-addresses.csv')
        print(f"📍 Loading addresses from {addresses_file}")
        
        addresses = {}
        try:
            with open(addresses_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    if limit and count >= limit:
                        break
                    
                    address_id = row['node_id']
                    address = {
                        'address_id': address_id,
                        'address': row['address'] or 'Unknown Address',
                        'name': row['name'] or '',
                        'countries': row['countries'] or 'Unknown',
                        'country_codes': row['country_codes'] or '',
                        'source': row['sourceID'] or 'Unknown',
                        'valid_until': row['valid_until'] or '',
                        'note': row['note'] or ''
                    }
                    addresses[address_id] = address
                    count += 1
            
            print(f"✅ Loaded {len(addresses):,} addresses")
            return addresses
            
        except Exception as e:
            print(f"❌ Error loading addresses: {e}")
            return {}
    
    def load_relationships(self, limit: int = None) -> List:
        """Load relationships from CSV"""
        relationships_file = os.path.join(self.data_dir, 'relationships.csv')
        print(f"🔗 Loading relationships from {relationships_file}")
        
        relationships = []
        try:
            with open(relationships_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    if limit and count >= limit:
                        break
                    
                    relationship = {
                        'start_node': row['node_id_start'],
                        'end_node': row['node_id_end'],
                        'rel_type': row['rel_type'] or 'connected_to',
                        'link': row['link'] or '',
                        'status': row['status'] or '',
                        'start_date': row['start_date'] or '',
                        'end_date': row['end_date'] or '',
                        'source': row['sourceID'] or 'Unknown'
                    }
                    relationships.append(relationship)
                    count += 1
            
            print(f"✅ Loaded {len(relationships):,} relationships")
            return relationships
            
        except Exception as e:
            print(f"❌ Error loading relationships: {e}")
            return []
    
    def load_all_data(self, entity_limit: int = 10000, officer_limit: int = 5000, 
                     address_limit: int = 5000, relationship_limit: int = 20000) -> Tuple[Dict, Dict, Dict, List]:
        """Load all ICIJ data with limits for performance"""
        print("\n🕵️ Loading Real ICIJ Offshore Leaks Data")
        print("=" * 60)
        
        # Load data with limits for performance
        self.entities = self.load_entities(entity_limit)
        self.officers = self.load_officers(officer_limit)
        self.addresses = self.load_addresses(address_limit)
        self.relationships = self.load_relationships(relationship_limit)
        
        print(f"\n📋 Summary:")
        print(f"   🏢 Entities: {len(self.entities):,}")
        print(f"   👥 Officers: {len(self.officers):,}")
        print(f"   📍 Addresses: {len(self.addresses):,}")
        print(f"   🔗 Relationships: {len(self.relationships):,}")
        
        # Analyze data sources
        self._analyze_data_sources()
        
        return self.entities, self.officers, self.addresses, self.relationships
    
    def _analyze_data_sources(self):
        """Analyze and report on data sources"""
        print(f"\n📊 Data Source Analysis:")
        
        # Entity sources
        entity_sources = {}
        for entity in self.entities.values():
            source = entity['source']
            entity_sources[source] = entity_sources.get(source, 0) + 1
        
        print(f"   Entity Sources:")
        for source, count in sorted(entity_sources.items(), key=lambda x: x[1], reverse=True):
            print(f"     📰 {source}: {count:,} entities")
        
        # Jurisdiction analysis
        jurisdictions = {}
        for entity in self.entities.values():
            jurisdiction = entity['jurisdiction']
            jurisdictions[jurisdiction] = jurisdictions.get(jurisdiction, 0) + 1
        
        print(f"\n   Top Jurisdictions:")
        for jurisdiction, count in sorted(jurisdictions.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"     🏝️ {jurisdiction}: {count:,} entities")
        
        # Officer countries
        officer_countries = {}
        for officer in self.officers.values():
            countries = officer['countries']
            officer_countries[countries] = officer_countries.get(countries, 0) + 1
        
        print(f"\n   Top Officer Countries:")
        for country, count in sorted(officer_countries.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"     🌍 {country}: {count:,} officers")
    
    def get_entity_by_id(self, entity_id: str) -> Dict:
        """Get entity by ID"""
        return self.entities.get(entity_id, {})
    
    def get_officer_by_id(self, officer_id: str) -> Dict:
        """Get officer by ID"""
        return self.officers.get(officer_id, {})
    
    def search_entities_by_name(self, name: str, limit: int = 10) -> List[Dict]:
        """Search entities by name"""
        name_lower = name.lower()
        matches = []
        
        for entity in self.entities.values():
            if name_lower in entity['name'].lower():
                matches.append(entity)
                if len(matches) >= limit:
                    break
        
        return matches
    
    def search_officers_by_name(self, name: str, limit: int = 10) -> List[Dict]:
        """Search officers by name"""
        name_lower = name.lower()
        matches = []
        
        for officer in self.officers.values():
            if name_lower in officer['name'].lower():
                matches.append(officer)
                if len(matches) >= limit:
                    break
        
        return matches

def test_real_icij_loader():
    """Test the real ICIJ data loader"""
    print("🧪 Testing Real ICIJ Data Loader")
    print("=" * 50)
    
    try:
        # Initialize loader
        loader = RealICIJDataLoader()
        
        # Load data with smaller limits for testing
        entities, officers, addresses, relationships = loader.load_all_data(
            entity_limit=1000, 
            officer_limit=500, 
            address_limit=500, 
            relationship_limit=2000
        )
        
        # Test search functionality
        print(f"\n🔍 Testing search functionality:")
        
        # Search for entities with 'CORP' in name
        corp_entities = loader.search_entities_by_name('CORP', limit=5)
        print(f"   Found {len(corp_entities)} entities with 'CORP' in name:")
        for entity in corp_entities[:3]:
            print(f"     🏢 {entity['name']} ({entity['jurisdiction']})")
        
        # Search for officers with common names
        john_officers = loader.search_officers_by_name('JOHN', limit=5)
        print(f"   Found {len(john_officers)} officers with 'JOHN' in name:")
        for officer in john_officers[:3]:
            print(f"     👤 {officer['name']} ({officer['countries']})")
        
        print(f"\n✅ Real ICIJ Data Loader test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_real_icij_loader()