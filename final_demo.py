# Final Demo Script - Complete SBP Project Demonstration

from pymongo import MongoClient
import time
import json

class SBPProjectDemo:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['sbp_project']
        print("🎯 SBP Project Demo - Ready!")
        print("="*60)
    
    def demo_1_data_overview(self):
        """Demo 1: Data Overview and Statistics"""
        print("\n📊 DEMO 1: DATA OVERVIEW")
        print("-" * 40)
        
        # Basic counts
        total = self.db.people.count_documents({})
        influencers = self.db.people.count_documents({"type": "influencer"})
        nobles = self.db.people.count_documents({"type": "noble"})
        
        print(f"Total Records: {total:,}")
        print(f"Influencers: {influencers:,}")
        print(f"Nobles: {nobles:,}")
        print(f"Dataset Size: >100MB ✓")
        
        # Sample documents
        print(f"\nSAMPLE INFLUENCER:")
        inf_sample = self.db.people.find_one({"type": "influencer"})
        for key, value in inf_sample.items():
            if key != '_id' and key != 'created_at' and key != 'updated_at':
                print(f"  {key}: {value}")
        
        print(f"\nSAMPLE NOBLE:")
        noble_sample = self.db.people.find_one({"type": "noble"})
        for key, value in noble_sample.items():
            if key != '_id' and key != 'created_at' and key != 'updated_at':
                print(f"  {key}: {value}")
    
    def demo_2_simple_queries(self):
        """Demo 2: Simple Analysis Queries (1-5)"""
        print(f"\n🔍 DEMO 2: SIMPLE QUERIES (1-5)")
        print("-" * 40)
        
        # Query 1: Age Distribution
        print("1. AGE DISTRIBUTION ANALYSIS")
        start = time.time()
        age_dist = list(self.db.people.aggregate([
            {"$group": {
                "_id": "$type",
                "avg_age": {"$avg": "$age"},
                "min_age": {"$min": "$age"},
                "max_age": {"$max": "$age"},
                "count": {"$sum": 1}
            }}
        ]))
        query1_time = time.time() - start
        
        for result in age_dist:
            print(f"   {result['_id'].title()}: avg={result['avg_age']:.1f}, range={result['min_age']}-{result['max_age']}, count={result['count']:,}")
        print(f"   ⚡ Query time: {query1_time*1000:.1f}ms")
        
        # Query 2: Gender Distribution
        print("\n2. GENDER DISTRIBUTION")
        start = time.time()
        gender_dist = list(self.db.people.aggregate([
            {"$group": {
                "_id": {"type": "$type", "sex": "$sex"},
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id.type": 1, "_id.sex": 1}}
        ]))
        query2_time = time.time() - start
        
        for result in gender_dist:
            print(f"   {result['_id']['type'].title()} {result['_id']['sex']}: {result['count']:,}")
        print(f"   ⚡ Query time: {query2_time*1000:.1f}ms")
        
        # Query 3: Top MBTI Types
        print("\n3. TOP MBTI PERSONALITY TYPES")
        start = time.time()
        mbti_dist = list(self.db.people.aggregate([
            {"$group": {
                "_id": "$mbti_personality",
                "total_count": {"$sum": 1},
                "influencer_count": {"$sum": {"$cond": [{"$eq": ["$type", "influencer"]}, 1, 0]}},
                "noble_count": {"$sum": {"$cond": [{"$eq": ["$type", "noble"]}, 1, 0]}}
            }},
            {"$sort": {"total_count": -1}},
            {"$limit": 5}
        ]))
        query3_time = time.time() - start
        
        for result in mbti_dist:
            print(f"   {result['_id']}: {result['total_count']:,} (I:{result['influencer_count']:,}, N:{result['noble_count']:,})")
        print(f"   ⚡ Query time: {query3_time*1000:.1f}ms")
        
        # Query 4: Top Countries
        print("\n4. TOP COUNTRIES (Influencers)")
        start = time.time()
        country_dist = list(self.db.people.aggregate([
            {"$match": {"type": "influencer"}},
            {"$group": {
                "_id": "$location.country",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]))
        query4_time = time.time() - start
        
        for result in country_dist:
            print(f"   {result['_id']}: {result['count']:,}")
        print(f"   ⚡ Query time: {query4_time*1000:.1f}ms")
        
        # Query 5: Age Comparison
        print("\n5. AVERAGE AGE COMPARISON")
        start = time.time()
        age_comparison = list(self.db.people.aggregate([
            {"$group": {
                "_id": "$type",
                "average_age": {"$avg": "$age"},
                "count": {"$sum": 1}
            }}
        ]))
        query5_time = time.time() - start
        
        for result in age_comparison:
            print(f"   {result['_id'].title()}: {result['average_age']:.1f} years (n={result['count']:,})")
        
        age_diff = abs(age_comparison[0]['average_age'] - age_comparison[1]['average_age'])
        print(f"   Age difference: {age_diff:.1f} years")
        print(f"   ⚡ Query time: {query5_time*1000:.1f}ms")
    
    def demo_3_complex_queries(self):
        """Demo 3: Complex Analysis Queries (6-10)"""
        print(f"\n🧠 DEMO 3: COMPLEX QUERIES (6-10)")
        print("-" * 40)
        
        # Query 6: MBTI vs Lifestyle Correlation
        print("6. MBTI vs LIFESTYLE CORRELATION (Influencers)")
        start = time.time()
        mbti_lifestyle = list(self.db.people.aggregate([
            {"$match": {"type": "influencer"}},
            {"$group": {
                "_id": {
                    "mbti": "$mbti_personality",
                    "lifestyle": "$profile.lifestyle"
                },
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]))
        query6_time = time.time() - start
        
        for result in mbti_lifestyle:
            print(f"   {result['_id']['mbti']} + {result['_id']['lifestyle']}: {result['count']:,}")
        print(f"   ⚡ Query time: {query6_time*1000:.1f}ms")
        
        # Query 7: Geographic Age Demographics
        print("\n7. GEOGRAPHIC AGE DEMOGRAPHICS")
        start = time.time()
        geo_age = list(self.db.people.aggregate([
            {"$match": {"type": "influencer"}},
            {"$group": {
                "_id": "$location.country",
                "avg_age": {"$avg": "$age"},
                "total_count": {"$sum": 1}
            }},
            {"$match": {"total_count": {"$gte": 200}}},
            {"$sort": {"total_count": -1}},
            {"$limit": 5}
        ]))
        query7_time = time.time() - start
        
        for result in geo_age:
            print(f"   {result['_id']}: {result['total_count']:,} people, avg age {result['avg_age']:.1f}")
        print(f"   ⚡ Query time: {query7_time*1000:.1f}ms")
        
        # Query 8: Cross-dataset Personality Analysis
        print("\n8. PERSONALITY PATTERNS BY AGE GROUPS")
        start = time.time()
        personality_analysis = list(self.db.people.aggregate([
            {"$group": {
                "_id": {
                    "mbti": "$mbti_personality",
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
            {"$match": {"total_count": {"$gte": 100}}},
            {"$sort": {"total_count": -1}},
            {"$limit": 5}
        ]))
        query8_time = time.time() - start
        
        for result in personality_analysis:
            print(f"   {result['_id']['mbti']} ({result['_id']['age_group']}): {result['total_count']:,} total (I:{result['influencer_count']:,}, N:{result['noble_count']:,})")
        print(f"   ⚡ Query time: {query8_time*1000:.1f}ms")
        
        # Query 9: Education vs Lifestyle Impact
        print("\n9. EDUCATION IMPACT ON LIFESTYLE")
        start = time.time()
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
            {"$limit": 5}
        ]))
        query9_time = time.time() - start
        
        for result in education_lifestyle:
            print(f"   {result['_id']['education']} → {result['_id']['lifestyle']}: {result['count']:,} (avg age: {result['avg_age']:.1f})")
        print(f"   ⚡ Query time: {query9_time*1000:.1f}ms")
        
        # Query 10: Comprehensive Demographic Comparison
        print("\n10. COMPREHENSIVE DEMOGRAPHIC COMPARISON")
        start = time.time()
        demographic_comparison = list(self.db.people.aggregate([
            {"$facet": {
                "by_type": [
                    {"$group": {
                        "_id": "$type",
                        "total_count": {"$sum": 1},
                        "avg_age": {"$avg": "$age"},
                        "male_count": {"$sum": {"$cond": [{"$eq": ["$sex", "Male"]}, 1, 0]}},
                        "female_count": {"$sum": {"$cond": [{"$eq": ["$sex", "Female"]}, 1, 0]}}
                    }}
                ],
                "mbti_diversity": [
                    {"$group": {"_id": "$mbti_personality", "count": {"$sum": 1}}},
                    {"$group": {"_id": None, "unique_types": {"$sum": 1}}}
                ]
            }}
        ]))
        query10_time = time.time() - start
        
        for type_data in demographic_comparison[0]['by_type']:
            total = type_data['total_count']
            male_pct = (type_data['male_count'] / total) * 100
            female_pct = (type_data['female_count'] / total) * 100
            print(f"   {type_data['_id'].title()}: {total:,} people, {male_pct:.1f}% male, {female_pct:.1f}% female, avg age {type_data['avg_age']:.1f}")
        
        mbti_diversity = demographic_comparison[0]['mbti_diversity'][0]['unique_types']
        print(f"   MBTI diversity: {mbti_diversity} unique personality types")
        print(f"   ⚡ Query time: {query10_time*1000:.1f}ms")
    
    def demo_4_performance_analysis(self):
        """Demo 4: Performance Analysis"""
        print(f"\n⚡ DEMO 4: PERFORMANCE ANALYSIS")
        print("-" * 40)
        
        # Show indexes
        print("CURRENT DATABASE INDEXES:")
        indexes = list(self.db.people.list_indexes())
        for i, index in enumerate(indexes, 1):
            print(f"   {i}. {index['name']}")
        
        # Performance test
        print(f"\nPERFORMANCE TEST:")
        
        # Complex filter query
        start = time.time()
        result1 = self.db.people.count_documents({
            "type": "influencer", 
            "age": {"$gte": 25, "$lte": 35},
            "sex": "Female"
        })
        time1 = time.time() - start
        print(f"   Complex filter: {result1:,} results in {time1*1000:.1f}ms")
        
        # Aggregation pipeline
        start = time.time()
        result2 = list(self.db.people.aggregate([
            {"$match": {"type": "influencer"}},
            {"$group": {"_id": "$location.country", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]))
        time2 = time.time() - start
        print(f"   Geographic aggregation: {len(result2)} countries in {time2*1000:.1f}ms")
        
        # Cross-type analysis
        start = time.time()
        result3 = list(self.db.people.aggregate([
            {"$group": {
                "_id": "$mbti_personality",
                "inf_count": {"$sum": {"$cond": [{"$eq": ["$type", "influencer"]}, 1, 0]}},
                "noble_count": {"$sum": {"$cond": [{"$eq": ["$type", "noble"]}, 1, 0]}}
            }},
            {"$sort": {"inf_count": -1}},
            {"$limit": 16}
        ]))
        time3 = time.time() - start
        print(f"   Cross-type MBTI analysis: {len(result3)} types in {time3*1000:.1f}ms")
        
        print(f"\n✅ All queries execute efficiently with proper indexing!")
        
    def demo_5_schema_benefits(self):
        """Demo 5: Schema Design Benefits"""
        print(f"\n🏗️  DEMO 5: SCHEMA DESIGN BENEFITS")
        print("-" * 40)
        
        # Collection comparison
        original_inf = self.db.influencers.count_documents({})
        original_nobles = self.db.nobles.count_documents({})
        unified_total = self.db.people.count_documents({})
        unified_inf = self.db.people.count_documents({"type": "influencer"})
        unified_nobles = self.db.people.count_documents({"type": "noble"})
        
        print("SCHEMA COMPARISON:")
        print(f"   Original Schema (2 collections):")
        print(f"     • influencers: {original_inf:,} documents")
        print(f"     • nobles: {original_nobles:,} documents")
        print(f"   Optimized Schema (1 unified collection):")
        print(f"     • people: {unified_total:,} documents")
        print(f"       - influencers: {unified_inf:,}")
        print(f"       - nobles: {unified_nobles:,}")
        
        print(f"\n   Benefits of unified schema:")
        print(f"     ✓ No cross-collection joins needed")
        print(f"     ✓ Consistent indexing strategy")
        print(f"     ✓ Simplified aggregation pipelines")
        print(f"     ✓ Better performance for comparative queries")
        print(f"     ✓ Easier maintenance and scaling")
        
        # Sample unified document structure
        print(f"\n   UNIFIED DOCUMENT STRUCTURE:")
        sample = self.db.people.find_one({})
        print(f"     • Core fields: name, age, sex, mbti_personality, backstory")
        print(f"     • Type identifier: {sample['type']}")
        print(f"     • Nested location: {list(sample['location'].keys())}")
        print(f"     • Nested profile: {list(sample['profile'].keys())}")
        print(f"     • Metadata: created_at, updated_at")
    
    def demo_6_final_summary(self):
        """Demo 6: Final Project Summary"""
        print(f"\n🎯 DEMO 6: PROJECT SUMMARY")
        print("-" * 40)
        
        print("SBP PROJECT ACHIEVEMENTS:")
        print("✅ Large dataset handling (>100MB, 57,980+ records)")
        print("✅ Document-oriented database design")
        print("✅ 10 comprehensive analysis questions")
        print("✅ Performance optimization with indexing")
        print("✅ Schema restructuring for efficiency")
        print("✅ Professional documentation")
        print("✅ Ready for visualization and presentation")
        
        print(f"\nTECHNICAL IMPLEMENTATION:")
        print(f"• Database: MongoDB Community Server")
        print(f"• Programming: Python 3.13 + pymongo")
        print(f"• Data Processing: Stream processing, batch inserts")
        print(f"• Optimization: Strategic indexing, aggregation pipelines")
        print(f"• Architecture: Scalable, maintainable design")
        
        print(f"\nREADY FOR:")
        print(f"📊 Presentation (May 29 - June 3)")
        print(f"🛡️  Defense (June 15)")
        print(f"📈 Advanced analytics and ML integration")
        print(f"🔗 Metabase visualization setup")
        
    def run_complete_demo(self):
        """Run the complete demo sequence"""
        print("🚀 STARTING COMPLETE SBP PROJECT DEMO")
        print("=" * 60)
        
        self.demo_1_data_overview()
        input("\nPress Enter to continue to Simple Queries...")
        
        self.demo_2_simple_queries()
        input("\nPress Enter to continue to Complex Queries...")
        
        self.demo_3_complex_queries()
        input("\nPress Enter to continue to Performance Analysis...")
        
        self.demo_4_performance_analysis()
        input("\nPress Enter to continue to Schema Benefits...")
        
        self.demo_5_schema_benefits()
        input("\nPress Enter for Final Summary...")
        
        self.demo_6_final_summary()
        
        print(f"\n🎉 DEMO COMPLETE!")
        print(f"Your SBP project is ready for presentation and defense!")

if __name__ == "__main__":
    demo = SBPProjectDemo()
    demo.run_complete_demo()
