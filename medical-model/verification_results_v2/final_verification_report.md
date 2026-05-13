# DeepSeek Verification Report - 204 Diseases (2026-05-08)

## Overall Results

| Batch | Diseases | APPROPRIATE | PARTIALLY | INAPPROPRIATE |
|-------|----------|-------------|-----------|---------------|
| 1     | 15       | 7           | 7         | 1             |
| 2     | 30       | 14          | 12        | 4             |
| 3     | 30       | 17          | 12        | 1             |
| 4     | 30       | 15          | 13        | 2             |
| 5     | 30       | 8           | 19        | 3             |
| 6     | 30       | 12          | 18        | 0             |
| 7     | 24       | 14          | 8         | 2             |
| **Total** | **204** | **87** | **89** | **13** |

## Summary Statistics

- **APPROPRIATE rate**: 42.6% (87/204)
- **PARTIALLY rate**: 43.6% (89/204)
- **INAPPROPRIATE rate**: 6.4% (13/204)
- **At least partially correct**: 94.6% (176/204)

## INAPPROPRIATE Diseases (Need Fix)

| Disease | Issue |
|---------|-------|
| 上呼吸道感染 | Antibiotics for viral URI |
| 子宫内膜异位症 | PPI/H2RA instead of endometriosis drugs |
| 宫颈炎 | Wrong antibiotics, not covering chlamydia/gonorrhea |
| 干眼症 | Glaucoma drugs instead of dry eye treatments |
| 强迫症 | Benzodiazepines instead of SSRIs for OCD |
| 病毒感染 | No antiviral drugs at all |
| 月经不调 | Iron/folic acid instead of hormonal regulation |
| 真菌感染 | Corticosteroids worsen fungal infections |
| 结肠癌 | Wrong chemotherapy drugs |
| 肺纤维化 | Steroids/epinephrine instead of antifibrotics |
| 白内障 | Glaucoma drugs instead of surgical management |
| 酗酒 | Benzodiazepines/antipsychotics instead of proper AUD treatment |
| 阴道炎 | Antibiotics not covering candida/trichomonas/gardnerella |

## Common PARTIALLY Issues

1. **Alprazolam contamination**: Benzodiazepine appearing in non-anxiety disorders (ADHD, Parkinson's, depression, OCD, smoking cessation)
2. **Amlodipine contamination**: Antihypertensive appearing in non-hypertension diseases (hypotension, cholesterol, PAH, hyperlipidemia)
3. **Cimetidine/PPI in wrong diseases**: Stomach drugs appearing in endometriosis, hemorrhoids, pancreatic cancer, fatty liver
4. **Wrong disease mapping**: Diseases mapped to incorrect proxy (e.g., 子宫内膜异位症→stomach pain, 胆囊炎→gout)

## Recommendations for Improvement

### Priority 1: Fix INAPPROPRIATE diseases
- Improve disease mapping for: 病毒感染, 真菌感染, 子宫内膜异位症, 阴道炎/宫颈炎, 月经不调
- Add safety filter rules for: corticosteroids in fungal infections, glaucoma drugs for cataract, antibiotics for viral conditions

### Priority 2: Fix PARTIALLY diseases
- Reduce Alprazolam contamination in non-anxiety disorders
- Reduce Amlodipine contamination in non-cardiovascular diseases
- Fix disease_mapper.py mappings: 子宫内膜异位症→stomach pain is wrong
- Fix SEMANTIC_VOCAB_MAP: 胆囊炎→gout mapping is wrong