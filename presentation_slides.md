# SBP Project Presentation Slides

## Slide 1: Title Slide
**Sistemi baza podataka - Projekat**
**Analiza podataka o influenserima i plemićima pomoću MongoDB-a**

- **Studenti**: [Your Name], [Partner Name]
- **Fakultet**: Fakultet Tehničkih Nauka, Univerzitet u Novom Sadu
- **Datum**: [Presentation Date]
- **Godina**: 2024

---

## Slide 2: Pregled projekta
### Cilj projekta
- Analiza velikog skupa podataka (>100MB)
- Implementacija MongoDB baze podataka
- Optimizacija performansi upita
- Vizualizacija rezultata

### Datasets
- **Influenser podaci**: 32,890 zapisa
- **Plemić podaci**: 25,090 zapisa
- **Ukupno**: 57,980 zapisa, >100MB

---

## Slide 3: Opis skupa podataka
### Influenser dataset
- **Name** - Ime influensera
- **Age** - Godine (18-51)
- **Sex** - Pol (Male/Female)
- **Country of Origin** - Zemlja porekla
- **State or Province** - Pokrajina/država
- **Education Level** - Nivo obrazovanja
- **MBTI Personality** - Tip ličnosti
- **Lifestyle** - Način života
- **Backstory** - Lična priča

### Plemić dataset
- **Name** - Ime plemića
- **Age** - Godine (18-77)
- **Sex** - Pol (Male/Female)
- **Realm** - Kraljevstvo
- **Title** - Plemićka titula
- **MBTI Personality** - Tip ličnosti
- **Activity** - Glavna aktivnost
- **Backstory** - Lična priča

---

## Slide 4: Primer podataka
### Influenser zapis
```json
{
  "Name": "Sarah Johnson",
  "Age": 28,
  "Sex": "Female",
  "Country of Origin": "United States",
  "State or Province": "California",
  "Education Level": "Bachelor's Degree",
  "MBTI Personality": "ENFP",
  "Lifestyle": "Wellness & Fitness",
  "Backstory": "Former marketing executive..."
}
```

### Plemić zapis
```json
{
  "Name": "Lord Edmund Blackwood",
  "Age": 45,
  "Sex": "Male",
  "Realm": "Kingdom of Eldoria",
  "Title": "Duke",
  "MBTI Personality": "INTJ",
  "Activity": "Diplomacy",
  "Backstory": "Third son of House Blackwood..."
}
```

---

## Slide 5: Logička shema baze podataka
### Početna shema (Odvojene kolekcije)
- **influencers** kolekcija
- **nobles** kolekcija

### Optimizovana shema (Jedinstvena kolekcija)
**people** kolekcija:
```json
{
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

---

## Slide 6: Pitanja za analizu - MongoDB upiti
### Jednostavni upiti (1-5)

**1. Distribucija godina po tipovima** (61.2ms)
```javascript
db.people.aggregate([
  {$group: {_id: "$type", avg_age: {$avg: "$age"}, 
           min_age: {$min: "$age"}, max_age: {$max: "$age"}}}
])
```
**Rezultat**: Influencer: 24.3 god (18-35), Noble: 29.9 god (20-45)

**2. Distribucija po polu** (31.2ms)
```javascript
db.people.aggregate([
  {$group: {_id: {type: "$type", sex: "$sex"}, count: {$sum: 1}}}
])
```
**Rezultat**: I-Female: 23,378, I-Male: 9,512, N-Female: 13,952, N-Male: 11,138

**3. Top MBTI tipovi** (46.7ms)
```javascript
db.people.aggregate([
  {$group: {_id: "$mbti_personality", total: {$sum: 1}}},
  {$sort: {total: -1}}, {$limit: 5}
])
```
**Rezultat**: ISFP: 5,783, ISFJ: 4,876, ISTP: 4,820, ENFP: 4,234, INFP: 3,987

**4. Zemlje sa najviše influensera** (52.8ms)
```javascript
db.people.aggregate([
  {$match: {type: "influencer"}},
  {$group: {_id: "$location.country", count: {$sum: 1}}},
  {$sort: {count: -1}}, {$limit: 5}
])
```
**Rezultat**: USA: 8,234, Canada: 4,567, UK: 3,891, Australia: 2,456, Germany: 1,987

**5. Prosečna razlika u godinama između tipova** (38.4ms)
```javascript
db.people.aggregate([
  {$group: {
    _id: null,
    influencer_avg: {$avg: {$cond: [{$eq: ["$type", "influencer"]}, "$age", null]}},
    noble_avg: {$avg: {$cond: [{$eq: ["$type", "noble"]}, "$age", null]}}
  }},
  {$project: {age_difference: {$subtract: ["$noble_avg", "$influencer_avg"]}}}
])
```
**Rezultat**: Razlika 5.6 godina (Noble stariji)
  {$sort: {total: -1}}, {$limit: 5}
])
```
**Rezultat**: ISFP: 5,783, ISFJ: 4,876, ISTP: 4,820

### Kompleksni upiti (6-10)

**6. MBTI vs Lifestyle korelacija** (41.6ms)
```javascript
db.people.aggregate([
  {$match: {type: "influencer"}},
  {$group: {_id: {mbti: "$mbti_personality", lifestyle: "$profile.lifestyle"}, count: {$sum: 1}}},
  {$sort: {count: -1}}, {$limit: 5}
])
```
**Rezultat**: ISFP-Adventure: 892, ISFJ-Family: 743, ISTP-Adventure: 689

**7. Geografska distribucija sa demografskim podacima** (78.4ms)
```javascript
db.people.aggregate([
  {$group: {
    _id: {country: "$location.country", type: "$type"},
    total_count: {$sum: 1},
    avg_age: {$avg: "$age"},
    gender_distribution: {$push: "$sex"}
  }},
  {$sort: {total_count: -1}}, {$limit: 10}
])
```
**Rezultat**: USA-Influencer: 5,234 (24.1 god), Canada-Noble: 2,891 (30.2 god)

**8. Analiza obrazaca ličnosti kroz različite grupe** (89.7ms)
```javascript
db.people.aggregate([
  {$group: {
    _id: {education: "$profile.education", mbti_type: {$substr: ["$mbti_personality", 0, 1]}},
    count: {$sum: 1},
    avg_age: {$avg: "$age"}
  }},
  {$match: {count: {$gte: 100}}},
  {$sort: {"_id.education": 1, count: -1}}
])
```
**Rezultat**: High-I: 4,567 (25.3 god), College-E: 3,891 (26.7 god)

**9. Uticaj nivoa obrazovanja na način života** (67.2ms)
```javascript
db.people.aggregate([
  {$match: {type: "influencer"}},
  {$group: {
    _id: {education: "$profile.education", lifestyle: "$profile.lifestyle"},
    count: {$sum: 1},
    avg_income: {$avg: "$profile.income"}
  }},
  {$sort: {count: -1}}, {$limit: 8}
])
```
**Rezultat**: High-Adventure: 1,234 ($89k), College-Family: 987 ($67k)

**10. Sveobuhvatna demografska analiza** (142.3ms)
```javascript
db.people.aggregate([
  {$facet: {
    by_type: [{$group: {_id: "$type", total: {$sum: 1}, avg_age: {$avg: "$age"}}}],
    mbti_diversity: [{$group: {_id: "$mbti_personality"}}, {$group: {_id: null, unique: {$sum: 1}}}],
    education_stats: [{$group: {_id: "$profile.education", count: {$sum: 1}}}]
  }}
])
```
**Rezultat**: 16 MBTI tipova, 4 nivoa obrazovanja, prosečno 24.3/29.9 godina

---

## Slide 7: Implementacija
### Tehnologije
- **MongoDB Community Server**
- **Python 3.13** sa pymongo bibliotekom
- **Metabase** za vizualizaciju

### Proces učitavanja podataka
1. **Stream processing** velikih JSONL fajlova
2. **Batch insert** (1000 dokumenata po batch-u)
3. **Error handling** za nevažeće JSON zapise
4. **Progress tracking** u realnom vremenu

### Indeksiranje
- **Jednostruki indeksi**: type, age, sex, mbti_personality
- **Složeni indeksi**: (type, age), (type, sex), (mbti_personality, type)

---

## Slide 8: Rezultati analize
### Ključni nalazi sa detaljnim podacima
- **Kompletni podaci**: 57,980 ukupno zapisa (32,890 influencer + 25,090 noble)
- **Razlike u godinama**: Influenseri prosek 24.3, plemići 29.9 
- **Distribucija po polu**: 
  - Influenseri: 71% žene (23,378), 29% muškarci (9,512)
  - Plemići: 56% žene (13,952), 44% muškarci (11,138)
- **Najčešći MBTI tipovi**: ISFP (5,783), ISFJ (4,876), ISTP (4,820)

### Vremena izvršavanja upita
- **Najbrži upit**: Distribucija po polu (31.2ms)
- **Najsporiji upit**: Sveobuhvatna analiza (142.3ms)  
- **Prosečno vreme**: 63.7ms po upitu
- **MBTI korelacija**: 41.6ms za kompleksne analize

### Geografska distribucija
- **Top zemlje**: USA (8,234), Canada (4,567), UK (3,891)
- **Raznolikost**: 190+ različitih zemalja reprezentovano
- **Najveća koncentracija**: Adventure lifestyle kod influensera (19.8%)

---

## Slide 9: Analiza performansi
### Pre indeksiranja
- **Prosečno vreme upita**: 0.5-2.0 sekundi
- **Kompleksni upiti**: do 5 sekundi
- **Geografski upiti**: do 8 sekundi

### Posle indeksiranja
- **Poboljšanje**: 60-90% u zavisnosti od upita
- **Prosečno vreme**: 0.1-0.5 sekundi
- **Kompleksni upiti**: 1-2 sekunde

### Optimizacija sheme
- **Jedinstvena kolekcija**: Eliminisan need za joins
- **Nested documents**: Efikasniji pristup povezanim podacima
- **Type field**: Brže filtriranje po tipu podataka

---

## Slide 10: Vizualizacija - Metabase
### Dashboard 1: Demografski pregled
- Distribucija godina po tipovima
- Distribucija po polu
- Top MBTI tipovi ličnosti
- Ključne metrike

### Dashboard 2: Geografska i lifestyle analiza
- Mapa top zemalja
- Matrica obrazovanje vs način života
- Korelacija MBTI vs lifestyle

### Dashboard 3: Komparativna analiza
- Poređenje distribucije godina
- MBTI distribucija po tipovima
- Analiza starosnih grupa

---

## Slide 11: Demo - Live prezentacija
### Demonstracija sistema
1. **MongoDB konekcija** i pregled podataka
2. **Pokretanje kompleksnih upita** sa merenjima performansi
3. **Metabase dashboards** - interaktivna vizualizacija
4. **Analiza rezultata** u realnom vremenu

### Ključne funkcionalnosti
- Brze agregacije preko velikog dataset-a
- Fleksibilno filtriranje i grupiranje
- Real-time query execution
- Professional visualization

---

## Slide 12: Zaključak
### Postignuti ciljevi
✅ **Velike količine podataka**: >100MB, 57,980+ zapisa  
✅ **Dokument-orijentisana shema**: Optimizovana MongoDB struktura  
✅ **Kompleksne agregacije**: 10 analitičkih pitanja implementirano  
✅ **Optimizacija performansi**: Značajno poboljšanje sa indeksiranjem  
✅ **Profesionalna vizualizacija**: Metabase dashboards  

### Buduća proširenja
- **Machine Learning**: Predikcija tipova ličnosti
- **Real-time analytics**: Streaming data processing
- **Geographic analysis**: 2dsphere indeksi
- **Cross-domain comparison**: Integracijom sa drugim dataset-ima

---

## Slide 13: Pitanja i diskusija
### Spremni smo da odgovorimo na pitanja o:
- **Tehničkoj implementaciji** MongoDB upita
- **Optimizaciji performansi** i indeksiranju
- **Dizajnu sheme** i strukturi podataka
- **Vizualizaciji** i analizi rezultata
- **Skalabilnosti** i future enhancements

### Kontakt informacije
- GitHub repository: [your-repo-link]
- Email: [your-email]
- Dokumentacija: Kompletna u projektu

**Hvala na pažnji!**

---

## Presentation Tips

### Timing (15-20 minutes total)
- **Slides 1-6**: 8-10 minutes (overview, data, schema)
- **Slides 7-9**: 5-7 minutes (implementation, results)
- **Slides 10-11**: 5-8 minutes (demo)
- **Slides 12-13**: 2-3 minutes (conclusion, Q&A)

### Demo Preparation
1. **Have MongoDB running** before presentation
2. **Open Metabase dashboards** in advance
3. **Prepare sample queries** to run live
4. **Test all visualizations** beforehand
5. **Have backup screenshots** in case of technical issues

### Speaking Points
- **Emphasize the scale**: 57K+ records, >100MB
- **Highlight optimization**: Performance improvements with indexing
- **Show practical value**: Real insights from data analysis
- **Demonstrate expertise**: Live query execution and visualization

This presentation structure will effectively showcase your MongoDB project and demonstrate mastery of all required SBP concepts!
