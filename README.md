# MongoDB Project - Influencer & Noble Data Analysis

## Project Overview
This project analyzes two datasets containing information about influencers and nobles, implementing a complete MongoDB-based data analysis pipeline.

### Datasets
- **Influencer Dataset**: 32,890 records with 9 fields
- **Noble Dataset**: 25,090 records with 8 fields
- **Total Size**: Combined datasets > 100MB
- **Combined Records**: 57,980 total records

### Data Schema Design

#### Original Schema (Per Collection)
**Influencers Collection:**
- Name (string)
- Age (number)
- Sex (string)
- Country of Origin (string)
- State or Province (string)
- Education Level (string)
- MBTI Personality (string)
- Lifestyle (string)
- Backstory (string)

**Nobles Collection:**
- Name (string)
- Age (number)
- Sex (string)
- Realm (string)
- Title (string)
- MBTI Personality (string)
- Activity (string)
- Backstory (string)

#### Optimized Schema (Unified Collection)
**People Collection:**
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
    "country": "string",
    "state_province": "string",
    "realm": "string"
  },
  "profile": {
    "education_level": "string",
    "lifestyle": "string",
    "title": "string",
    "activity": "string"
  },
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

## 10 Analysis Questions

### Simple Queries (5):
1. What is the age distribution across both datasets?
2. How many people are there per gender in each dataset?
3. What are the most common MBTI personality types?
4. Which countries have the most influencers?
5. What is the average age difference between influencers and nobles?

### Complex Queries (5):
6. Correlation between MBTI personality types and lifestyle choices for influencers
7. Geographic distribution analysis with age demographics
8. Cross-dataset personality pattern analysis by gender and age groups
9. Education level impact on lifestyle choices among influencers
10. Comprehensive demographic comparison between influencers and nobles

## Implementation Steps
1. Data Loading and Schema Design
2. Query Implementation and Analysis
3. Performance Analysis
4. Schema Optimization
5. Index Creation
6. Performance Comparison
7. Metabase Visualization
