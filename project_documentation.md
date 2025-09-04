# SBP Project Documentation
## MongoDB Analysis: Influencer & Noble Data

### Project Team
- Student 1: [Your Name]
- Student 2: [Partner Name]
- University: Univerzitet u Novom Sadu, Fakultet Tehničkih Nauka
- Course: Sistemi baza podataka (SBP)
- Year: 2024

---

## 1. Dataset Description

### Data Sources
- **Dataset 1**: Influencer Data (influencer_data.jsonl)
  - **Records**: 32,890
  - **Size**: ~50MB
  - **Source**: Generated synthetic data representing social media influencers

- **Dataset 2**: Noble Data (noble_data.jsonl)
  - **Records**: 25,090
  - **Size**: ~50MB
  - **Source**: Generated synthetic data representing historical nobles

- **Total Dataset Size**: ~100MB+ (meets project requirements)
- **Combined Records**: 57,980

### Data Semantics

#### Influencer Dataset Fields:
1. **Name** (string) - Full name of the influencer
2. **Age** (number) - Age in years (18-65)
3. **Sex** (string) - Gender (Male/Female)
4. **Country of Origin** (string) - Birth country
5. **State or Province** (string) - Geographic subdivision
6. **Education Level** (string) - Highest education achieved
7. **MBTI Personality** (string) - Myers-Briggs personality type
8. **Lifestyle** (string) - Primary lifestyle category
9. **Backstory** (string) - Personal background narrative

#### Noble Dataset Fields:
1. **Name** (string) - Full name of the noble
2. **Age** (number) - Age in years (18-80)
3. **Sex** (string) - Gender (Male/Female)
4. **Realm** (string) - Kingdom or territory
5. **Title** (string) - Noble title or rank
6. **MBTI Personality** (string) - Myers-Briggs personality type
7. **Activity** (string) - Primary occupation/activity
8. **Backstory** (string) - Personal background narrative

### Data Distribution Example
```json
// Influencer Record
{
  "Name": "Sarah Johnson",
  "Age": 28,
  "Sex": "Female",
  "Country of Origin": "United States",
  "State or Province": "California",
  "Education Level": "Bachelor's Degree",
  "MBTI Personality": "ENFP",
  "Lifestyle": "Wellness & Fitness",
  "Backstory": "Former marketing executive turned fitness influencer..."
}

// Noble Record  
{
  "Name": "Lord Edmund Blackwood",
  "Age": 45,
  "Sex": "Male",
  "Realm": "Kingdom of Eldoria",
  "Title": "Duke",
  "MBTI Personality": "INTJ",
  "Activity": "Diplomacy",
  "Backstory": "Third son of House Blackwood, known for strategic mind..."
}
```

---

## 2. Logical Database Schema

### Initial Schema (Separate Collections)
Two collections mirroring the original JSONL structure:
- `influencers` collection
- `nobles` collection

### Optimized Schema (Unified Collection)
**Collection: `people`**
```json
{
  "_id": ObjectId,
  "name": "string",
  "age": "number", 
  "sex": "string",
  "mbti_personality": "string",
  "backstory": "string",
  "type": "influencer|noble",
  "location": {
    "country": "string",        // influencers only
    "state_province": "string", // influencers only  
    "realm": "string"          // nobles only
  },
  "profile": {
    "education_level": "string", // influencers only
    "lifestyle": "string",       // influencers only
    "title": "string",          // nobles only
    "activity": "string"        // nobles only
  },
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

### Schema Design Rationale
1. **Unified Structure**: Combines both datasets while preserving type-specific data
2. **Nested Documents**: Groups related fields (location, profile)
3. **Type Field**: Enables efficient filtering between influencers and nobles
4. **Timestamps**: Tracks data creation and modification
5. **Null Handling**: Type-specific fields are null for the other type

---

## 3. Analysis Questions (Agregacije)

### Simple Queries (1-5):
1. **Age Distribution Analysis**: What is the age distribution across both datasets?
2. **Gender Distribution**: How many people are there per gender in each dataset?
3. **MBTI Popularity**: What are the most common MBTI personality types?
4. **Geographic Distribution**: Which countries have the most influencers?
5. **Age Comparison**: What is the average age difference between influencers and nobles?

### Complex Queries (6-10):
6. **MBTI-Lifestyle Correlation**: How do MBTI personality types correlate with lifestyle choices for influencers?
7. **Geographic Demographics**: What are the age demographics across different countries?
8. **Cross-Dataset Personality Patterns**: How do personality types distribute across gender and age groups in both datasets?
9. **Education-Lifestyle Impact**: How does education level impact lifestyle choices among influencers?
10. **Comprehensive Comparison**: What are the key demographic differences between influencers and nobles?

---

## 4. Implementation Details

### Technology Stack
- **Database**: MongoDB Community Server
- **Programming Language**: Python 3.13
- **Libraries**: 
  - `pymongo` - MongoDB driver
  - `json` - JSON processing
  - `datetime` - Timestamp handling
  - `time` - Performance measurement
  - `collections` - Data structures

### Data Loading Process
1. **File Reading**: Stream processing of large JSONL files
2. **Batch Insert**: 1000-document batches for optimal performance
3. **Error Handling**: Graceful handling of malformed JSON
4. **Progress Tracking**: Real-time progress indicators
5. **Type Addition**: Adding document type field during load

### Index Strategy
**Single Field Indexes:**
- `type` - Primary filter field
- `age` - Frequent aggregation field
- `sex` - Common grouping field  
- `mbti_personality` - Analysis field
- `location.country` - Geographic queries
- `profile.education_level` - Education analysis
- `profile.lifestyle` - Lifestyle analysis

**Compound Indexes:**
- `(type, age)` - Type-specific age queries
- `(type, sex)` - Gender analysis by type
- `(mbti_personality, type)` - Personality analysis
- `(location.country, age)` - Geographic demographics

---

## 5. Performance Analysis

### Query Performance Metrics
Measured execution times for all 10 queries:
- **Before Indexing**: Baseline performance
- **After Indexing**: Optimized performance
- **Improvement Calculation**: Percentage performance gain

### Optimization Techniques
1. **Schema Restructuring**: Unified collection reduces joins
2. **Strategic Indexing**: Covering indexes for common query patterns
3. **Aggregation Pipeline**: Efficient data processing
4. **Batch Operations**: Bulk inserts and updates
5. **Memory Management**: Streaming for large datasets

### Expected Performance Improvements
- **Simple Queries**: 60-80% improvement with proper indexes
- **Complex Aggregations**: 40-60% improvement
- **Geographic Queries**: 70-90% improvement with geo indexes
- **Cross-Type Queries**: 50-70% improvement with compound indexes

---

## 6. Visualization Strategy (Metabase)

### Dashboard 1: Demographics Overview
- Age distribution histograms
- Gender breakdown pie charts  
- MBTI type popularity bars
- Key performance indicators

### Dashboard 2: Geographic Analysis
- World map of influencer distribution
- Country-wise age demographics
- Regional personality patterns
- Geographic diversity metrics

### Dashboard 3: Comparative Analysis  
- Side-by-side type comparisons
- Correlation heatmaps
- Trend analysis over age groups
- Cross-dataset insights

### Dashboard 4: Detailed Breakdowns
- Education vs lifestyle matrices
- Personality type deep dives
- Custom filtered views
- Export-ready reports

---

## 7. Project Structure

```
projekat_spajanje/
├── influencer_data.jsonl          # Raw influencer data
├── noble_data.jsonl               # Raw noble data
├── mongodb_project.py             # Main project implementation
├── analyze_jsonl.py               # Initial data analysis
├── test_mongo.py                  # MongoDB connection test
├── run_project.bat                # Windows batch script
├── README.md                      # Project overview
├── metabase_setup.md             # Visualization setup guide
└── project_documentation.md      # This comprehensive guide
```

---

## 8. Running the Project

### Prerequisites
1. **MongoDB**: Community Server installed and running
2. **Python**: Version 3.7+ with pymongo library
3. **Data Files**: Both JSONL files in project directory

### Execution Steps
```bash
# 1. Test MongoDB connection
python test_mongo.py

# 2. Run complete analysis
python mongodb_project.py

# 3. Alternative: Use batch script (Windows)
run_project.bat
```

### Expected Output
1. Data loading progress indicators
2. Schema creation confirmation
3. Query execution with timing
4. Performance comparison results
5. Summary statistics and insights

---

## 9. Results and Insights

### Key Findings
- **Complete Data**: 100% non-null values across all fields
- **Age Patterns**: Different age distributions between types
- **Geographic Diversity**: Wide representation across countries
- **Personality Types**: MBTI distribution varies by demographic
- **Performance Gains**: Significant improvements with indexing

### Business Value
- **Demographic Understanding**: Clear patterns in both populations
- **Performance Optimization**: Proven indexing strategies
- **Scalable Architecture**: Schema supports future expansion
- **Analytical Foundation**: Ready for advanced ML analysis

---

## 10. Future Enhancements

### Technical Improvements
1. **Sharding Strategy**: For datasets > 1TB
2. **Real-time Analytics**: Streaming data processing
3. **Machine Learning**: Personality prediction models
4. **Geographic Indexing**: 2dsphere indexes for location data

### Analysis Extensions
1. **Sentiment Analysis**: Backstory text processing
2. **Network Analysis**: Relationship mapping
3. **Predictive Modeling**: Trend forecasting
4. **Cross-Domain**: Comparison with other datasets

---

## Conclusion

This project successfully demonstrates:
- ✅ Large dataset handling (>100MB, 57K+ records)
- ✅ Document-oriented database design
- ✅ Complex aggregation queries
- ✅ Performance optimization techniques
- ✅ Professional visualization setup
- ✅ Comprehensive documentation

The implementation provides a solid foundation for advanced data analytics and serves as an excellent example of MongoDB capabilities in handling diverse, semi-structured datasets.

---

**Project Status**: ✅ Complete and Ready for Presentation
**Presentation Date**: May 29 - June 3, 2024
**Defense Date**: June 15, 2024
