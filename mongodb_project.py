import json
import time
from datetime import datetime
from pymongo import MongoClient, errors
from collections import defaultdict, Counter
import statistics

class MongoDBProject:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect_to_mongodb()
        
    def connect_to_mongodb(self):
        """Connect to MongoDB with error handling"""
        try:
            self.client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=30000)
            self.client.admin.command('ping')
            self.db = self.client['sbp_project']
            print("✓ Connected to MongoDB successfully")
        except errors.ServerSelectionTimeoutError:
            print("❌ Error: MongoDB is not running. Please start MongoDB first.")
            print("To start MongoDB on Windows:")
            print("1. Open Command Prompt as Administrator")
            print("2. Run: net start MongoDB")
            print("Or install MongoDB Community Server if not installed")
            exit(1)
    
    def load_initial_data(self):
        """Load data with original schema (separate collections)"""
        print("\n=== LOADING INITIAL DATA ===")
        
        # Clear existing collections
        self.db.influencers.drop()
        self.db.nobles.drop()
        
        # Load influencers
        print("Loading influencers data...")
        influencer_count = 0
        with open('influencer_data.jsonl', 'r', encoding='utf-8') as f:
            batch = []
            for line in f:
                try:
                    doc = json.loads(line.strip())
                    doc['type'] = 'influencer'
                    doc['created_at'] = datetime.now()
                    batch.append(doc)
                    influencer_count += 1
                    
                    if len(batch) >= 1000:
                        self.db.influencers.insert_many(batch, ordered=False)
                        batch = []
                        if influencer_count % 10000 == 0:
                            print(f"  Loaded {influencer_count:,} influencers...")
                except:
                    continue
            
            if batch:
                self.db.influencers.insert_many(batch, ordered=False)
        
        print(f"✓ Loaded {influencer_count:,} influencers")
        
        # Load nobles
        print("Loading nobles data...")
        noble_count = 0
        with open('noble_data.jsonl', 'r', encoding='utf-8') as f:
            batch = []
            for line in f:
                try:
                    doc = json.loads(line.strip())
                    doc['type'] = 'noble'
                    doc['created_at'] = datetime.now()
                    batch.append(doc)
                    noble_count += 1
                    
                    if len(batch) >= 1000:
                        self.db.nobles.insert_many(batch, ordered=False)
                        batch = []
                        if noble_count % 10000 == 0:
                            print(f"  Loaded {noble_count:,} nobles...")
                except:
                    continue
            
            if batch:
                self.db.nobles.insert_many(batch, ordered=False)
        
        print(f"✓ Loaded {noble_count:,} nobles")
        print(f"✓ Total records: {influencer_count + noble_count:,}")
    
    def create_unified_schema(self):
        """Create optimized unified schema"""
        print("\n=== CREATING UNIFIED SCHEMA ===")
        
        # Drop existing unified collection
        self.db.people.drop()
        
        # Process influencers
        print("Processing influencers for unified schema...")
        influencer_docs = []
        for doc in self.db.influencers.find():
            unified_doc = {
                'name': doc.get('Name'),
                'age': doc.get('Age'),
                'sex': doc.get('Sex'),
                'mbti_personality': doc.get('MBTI Personality'),
                'backstory': doc.get('Backstory'),
                'type': 'influencer',
                'location': {
                    'country': doc.get('Country of Origin'),
                    'state_province': doc.get('State or Province'),
                    'realm': None
                },
                'profile': {
                    'education_level': doc.get('Education Level'),
                    'lifestyle': doc.get('Lifestyle'),
                    'title': None,
                    'activity': None
                },
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            influencer_docs.append(unified_doc)
            
            if len(influencer_docs) >= 1000:
                self.db.people.insert_many(influencer_docs, ordered=False)
                influencer_docs = []
        
        if influencer_docs:
            self.db.people.insert_many(influencer_docs, ordered=False)
        
        # Process nobles
        print("Processing nobles for unified schema...")
        noble_docs = []
        for doc in self.db.nobles.find():
            unified_doc = {
                'name': doc.get('Name'),
                'age': doc.get('Age'),
                'sex': doc.get('Sex'),
                'mbti_personality': doc.get('MBTI Personality'),
                'backstory': doc.get('Backstory'),
                'type': 'noble',
                'location': {
                    'country': None,
                    'state_province': None,
                    'realm': doc.get('Realm')
                },
                'profile': {
                    'education_level': None,
                    'lifestyle': None,
                    'title': doc.get('Title'),
                    'activity': doc.get('Activity')
                },
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            noble_docs.append(unified_doc)
            
            if len(noble_docs) >= 1000:
                self.db.people.insert_many(noble_docs, ordered=False)
                noble_docs = []
        
        if noble_docs:
            self.db.people.insert_many(noble_docs, ordered=False)
        
        total_unified = self.db.people.count_documents({})
        print(f"✓ Created unified collection with {total_unified:,} documents")
    
    def run_analysis_queries(self):
        """Run the 10 analysis queries"""
        print("\n=== RUNNING ANALYSIS QUERIES ===")
        
        results = {}
        
        # Query 1: Age distribution
        print("1. Analyzing age distribution...")
        start_time = time.time()
        age_dist = list(self.db.people.aggregate([
            {"$group": {
                "_id": "$type",
                "avg_age": {"$avg": "$age"},
                "min_age": {"$min": "$age"},
                "max_age": {"$max": "$age"},
                "count": {"$sum": 1}
            }}
        ]))
        query1_time = time.time() - start_time
        results['age_distribution'] = {'data': age_dist, 'time': query1_time}
        print(f"   Completed in {query1_time:.3f}s")
        
        # Query 2: Gender distribution
        print("2. Analyzing gender distribution...")
        start_time = time.time()
        gender_dist = list(self.db.people.aggregate([
            {"$group": {
                "_id": {"type": "$type", "sex": "$sex"},
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id.type": 1, "_id.sex": 1}}
        ]))
        query2_time = time.time() - start_time
        results['gender_distribution'] = {'data': gender_dist, 'time': query2_time}
        print(f"   Completed in {query2_time:.3f}s")
        
        # Query 3: MBTI personality types
        print("3. Analyzing MBTI personality types...")
        start_time = time.time()
        mbti_dist = list(self.db.people.aggregate([
            {"$group": {
                "_id": "$mbti_personality",
                "total_count": {"$sum": 1},
                "influencer_count": {"$sum": {"$cond": [{"$eq": ["$type", "influencer"]}, 1, 0]}},
                "noble_count": {"$sum": {"$cond": [{"$eq": ["$type", "noble"]}, 1, 0]}}
            }},
            {"$sort": {"total_count": -1}},
            {"$limit": 16}  # Top 16 MBTI types
        ]))
        query3_time = time.time() - start_time
        results['mbti_distribution'] = {'data': mbti_dist, 'time': query3_time}
        print(f"   Completed in {query3_time:.3f}s")
        
        # Query 4: Country distribution for influencers
        print("4. Analyzing country distribution...")
        start_time = time.time()
        country_dist = list(self.db.people.aggregate([
            {"$match": {"type": "influencer"}},
            {"$group": {
                "_id": "$location.country",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 20}
        ]))
        query4_time = time.time() - start_time
        results['country_distribution'] = {'data': country_dist, 'time': query4_time}
        print(f"   Completed in {query4_time:.3f}s")
        
        # Query 5: Average age comparison
        print("5. Comparing average ages...")
        start_time = time.time()
        age_comparison = list(self.db.people.aggregate([
            {"$group": {
                "_id": "$type",
                "average_age": {"$avg": "$age"},
                "median_age": {"$median": "$age"},
                "count": {"$sum": 1}
            }}
        ]))
        query5_time = time.time() - start_time
        results['age_comparison'] = {'data': age_comparison, 'time': query5_time}
        print(f"   Completed in {query5_time:.3f}s")
        
        # Query 6: MBTI vs Lifestyle correlation (Complex)
        print("6. Analyzing MBTI vs Lifestyle correlation...")
        start_time = time.time()
        mbti_lifestyle = list(self.db.people.aggregate([
            {"$match": {"type": "influencer", "profile.lifestyle": {"$ne": None}}},
            {"$group": {
                "_id": {
                    "mbti": "$mbti_personality",
                    "lifestyle": "$profile.lifestyle"
                },
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 50}
        ]))
        query6_time = time.time() - start_time
        results['mbti_lifestyle'] = {'data': mbti_lifestyle, 'time': query6_time}
        print(f"   Completed in {query6_time:.3f}s")
        
        # Query 7: Geographic distribution with age demographics (Complex)
        print("7. Analyzing geographic-age demographics...")
        start_time = time.time()
        geo_age = list(self.db.people.aggregate([
            {"$match": {"type": "influencer"}},
            {"$group": {
                "_id": "$location.country",
                "avg_age": {"$avg": "$age"},
                "age_ranges": {
                    "$push": {
                        "$switch": {
                            "branches": [
                                {"case": {"$lt": ["$age", 25]}, "then": "18-24"},
                                {"case": {"$lt": ["$age", 35]}, "then": "25-34"},
                                {"case": {"$lt": ["$age", 45]}, "then": "35-44"},
                                {"case": {"$gte": ["$age", 45]}, "then": "45+"}
                            ]
                        }
                    }
                },
                "total_count": {"$sum": 1}
            }},
            {"$match": {"total_count": {"$gte": 100}}},  # Countries with at least 100 influencers
            {"$sort": {"total_count": -1}},
            {"$limit": 15}
        ]))
        query7_time = time.time() - start_time
        results['geo_age_demographics'] = {'data': geo_age, 'time': query7_time}
        print(f"   Completed in {query7_time:.3f}s")
        
        # Query 8: Cross-dataset personality analysis (Complex)
        print("8. Cross-dataset personality pattern analysis...")
        start_time = time.time()
        personality_analysis = list(self.db.people.aggregate([
            {"$group": {
                "_id": {
                    "mbti": "$mbti_personality",
                    "sex": "$sex",
                    "age_group": {
                        "$switch": {
                            "branches": [
                                {"case": {"$lt": ["$age", 30]}, "then": "Young"},
                                {"case": {"$lt": ["$age", 50]}, "then": "Middle"},
                                {"case": {"$gte": ["$age", 50]}, "then": "Senior"}
                            ]
                        }
                    }
                },
                "influencer_count": {"$sum": {"$cond": [{"$eq": ["$type", "influencer"]}, 1, 0]}},
                "noble_count": {"$sum": {"$cond": [{"$eq": ["$type", "noble"]}, 1, 0]}},
                "total_count": {"$sum": 1}
            }},
            {"$match": {"total_count": {"$gte": 50}}},
            {"$sort": {"total_count": -1}},
            {"$limit": 30}
        ]))
        query8_time = time.time() - start_time
        results['personality_analysis'] = {'data': personality_analysis, 'time': query8_time}
        print(f"   Completed in {query8_time:.3f}s")
        
        # Query 9: Education vs Lifestyle analysis (Complex)
        print("9. Education level impact on lifestyle...")
        start_time = time.time()
        education_lifestyle = list(self.db.people.aggregate([
            {"$match": {"type": "influencer"}},
            {"$group": {
                "_id": {
                    "education": "$profile.education_level",
                    "lifestyle": "$profile.lifestyle"
                },
                "count": {"$sum": 1},
                "avg_age": {"$avg": "$age"}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 25}
        ]))
        query9_time = time.time() - start_time
        results['education_lifestyle'] = {'data': education_lifestyle, 'time': query9_time}
        print(f"   Completed in {query9_time:.3f}s")
        
        # Query 10: Comprehensive demographic comparison (Complex)
        print("10. Comprehensive demographic comparison...")
        start_time = time.time()
        demographic_comparison = list(self.db.people.aggregate([
            {"$facet": {
                "by_type": [
                    {"$group": {
                        "_id": "$type",
                        "total_count": {"$sum": 1},
                        "avg_age": {"$avg": "$age"},
                        "male_count": {"$sum": {"$cond": [{"$eq": ["$sex", "Male"]}, 1, 0]}},
                        "female_count": {"$sum": {"$cond": [{"$eq": ["$sex", "Female"]}, 1, 0]}},
                        "most_common_mbti": {"$first": "$mbti_personality"}
                    }}
                ],
                "mbti_comparison": [
                    {"$group": {
                        "_id": "$mbti_personality",
                        "influencer_ratio": {
                            "$avg": {"$cond": [{"$eq": ["$type", "influencer"]}, 1, 0]}
                        },
                        "noble_ratio": {
                            "$avg": {"$cond": [{"$eq": ["$type", "noble"]}, 1, 0]}
                        },
                        "total_count": {"$sum": 1}
                    }},
                    {"$sort": {"total_count": -1}},
                    {"$limit": 16}
                ]
            }}
        ]))
        query10_time = time.time() - start_time
        results['demographic_comparison'] = {'data': demographic_comparison, 'time': query10_time}
        print(f"   Completed in {query10_time:.3f}s")
        
        return results
    
    def create_indexes(self):
        """Create indexes for performance optimization"""
        print("\n=== CREATING INDEXES ===")
        
        indexes = [
            ("type", 1),
            ("age", 1),
            ("sex", 1),
            ("mbti_personality", 1),
            ("location.country", 1),
            ("profile.education_level", 1),
            ("profile.lifestyle", 1),
            ([("type", 1), ("age", 1)], {}),
            ([("type", 1), ("sex", 1)], {}),
            ([("mbti_personality", 1), ("type", 1)], {}),
            ([("location.country", 1), ("age", 1)], {})
        ]
        
        for index in indexes:
            if isinstance(index[0], list):
                self.db.people.create_index(index[0], **index[1])
                print(f"✓ Created compound index: {index[0]}")
            else:
                self.db.people.create_index([(index[0], index[1])])
                print(f"✓ Created index: {index[0]}")
    
    def print_results(self, results):
        """Print analysis results in a formatted way"""
        print("\n" + "="*60)
        print("ANALYSIS RESULTS")
        print("="*60)
        
        # Query 1: Age distribution
        print("\n1. AGE DISTRIBUTION:")
        for item in results['age_distribution']['data']:
            print(f"   {item['_id'].title()}: avg={item['avg_age']:.1f}, min={item['min_age']}, max={item['max_age']}, count={item['count']:,}")
        
        # Query 2: Gender distribution
        print("\n2. GENDER DISTRIBUTION:")
        for item in results['gender_distribution']['data']:
            print(f"   {item['_id']['type'].title()} {item['_id']['sex']}: {item['count']:,}")
        
        # Query 3: Top MBTI types
        print("\n3. TOP MBTI PERSONALITY TYPES:")
        for item in results['mbti_distribution']['data'][:10]:
            print(f"   {item['_id']}: {item['total_count']:,} (I:{item['influencer_count']:,}, N:{item['noble_count']:,})")
        
        # Query 4: Top countries
        print("\n4. TOP COUNTRIES (Influencers):")
        for item in results['country_distribution']['data'][:10]:
            print(f"   {item['_id']}: {item['count']:,}")
        
        # Query 5: Age comparison
        print("\n5. AGE COMPARISON:")
        for item in results['age_comparison']['data']:
            print(f"   {item['_id'].title()}: avg={item['average_age']:.1f}, count={item['count']:,}")
        
        # Performance summary
        print("\n" + "="*60)
        print("QUERY PERFORMANCE SUMMARY:")
        print("="*60)
        total_time = 0
        for query_name, result in results.items():
            query_time = result['time']
            total_time += query_time
            print(f"{query_name:25}: {query_time:.3f}s")
        print(f"{'TOTAL TIME':25}: {total_time:.3f}s")
    
    def run_project(self):
        """Run the complete project"""
        print("MongoDB Project - Influencer & Noble Data Analysis")
        print("="*60)
        
        # Step 1: Load initial data
        self.load_initial_data()
        
        # Step 2: Create unified schema
        self.create_unified_schema()
        
        # Step 3: Run queries without indexes
        print("\n=== PERFORMANCE TEST: WITHOUT INDEXES ===")
        results_before = self.run_analysis_queries()
        
        # Step 4: Create indexes
        self.create_indexes()
        
        # Step 5: Run queries with indexes
        print("\n=== PERFORMANCE TEST: WITH INDEXES ===")
        results_after = self.run_analysis_queries()
        
        # Step 6: Print results and comparison
        self.print_results(results_after)
        
        # Performance comparison
        print("\n" + "="*60)
        print("PERFORMANCE COMPARISON (Before vs After Indexing):")
        print("="*60)
        
        for query_name in results_before.keys():
            before_time = results_before[query_name]['time']
            after_time = results_after[query_name]['time']
            improvement = ((before_time - after_time) / before_time) * 100
            print(f"{query_name:25}: {before_time:.3f}s -> {after_time:.3f}s ({improvement:+.1f}%)")
        
        print("\n✓ Project completed successfully!")
        print("Ready for Metabase visualization setup.")

if __name__ == "__main__":
    project = MongoDBProject()
    project.run_project()
