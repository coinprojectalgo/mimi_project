"""
Knowledge Base — Curated disease information for RAG pipeline.
Provides detailed context about each disease for the LLM to use
when generating diagnoses and remedies.
"""

DISEASE_KNOWLEDGE = {
    "Apple - Apple Scab": {
        "crop": "Apple",
        "disease": "Apple Scab",
        "pathogen": "Venturia inaequalis (fungus)",
        "symptoms": "Olive-green to dark brown velvety spots on leaves. Leaves may curl, yellow, and drop early. Fruit develops raised, corky, dark lesions that crack over time.",
        "causes": "Fungal spores overwinter in fallen leaves and release during wet spring weather. Spread by rain splash and wind.",
        "favorable_conditions": "Cool, wet spring weather (15-25°C). Prolonged leaf wetness (>9 hours). High humidity above 70%.",
        "organic_remedies": [
            "Apply neem oil spray (2-3%) during early season",
            "Use sulfur-based fungicides as preventive",
            "Remove and destroy fallen infected leaves",
            "Improve air circulation through pruning",
            "Apply compost tea as foliar spray"
        ],
        "chemical_treatments": [
            "Mancozeb 75% WP at 2.5g/L as preventive spray",
            "Myclobutanil (Systhane) at recommended dosage",
            "Captan 50% WP at 2g/L during petal fall",
            "Dodine 65% WP for severe infections"
        ],
        "prevention": [
            "Plant scab-resistant apple varieties (Liberty, Enterprise)",
            "Maintain proper tree spacing for air flow",
            "Clean up fallen leaves in autumn",
            "Apply dormant sprays before bud break",
            "Avoid overhead irrigation"
        ],
        "severity": "Medium to High — can cause significant yield and quality loss if untreated"
    },
    "Apple - Black Rot": {
        "crop": "Apple",
        "disease": "Black Rot",
        "pathogen": "Botryosphaeria obtusa (fungus)",
        "symptoms": "Frogeye leaf spots — circular brown lesions with purple margins. Fruit rot starts as brown spots expanding into large black, firm, rotted areas. Cankers on branches with rough, cracked bark.",
        "causes": "Fungus survives in mummified fruits, dead bark, and cankers. Enters through wounds or natural openings.",
        "favorable_conditions": "Warm, humid weather (20-30°C). Trees weakened by drought or winter injury. Poor sanitation practices.",
        "organic_remedies": [
            "Remove and destroy mummified fruits and cankered branches",
            "Apply copper-based fungicides (Bordeaux mixture) in dormant season",
            "Neem oil applications during growing season",
            "Improve tree vigor through balanced fertilization"
        ],
        "chemical_treatments": [
            "Thiophanate-methyl (Topsin-M) at 1g/L",
            "Captan 50% WP at 2g/L during bloom",
            "Mancozeb as protective spray at 2.5g/L",
            "Pyraclostrobin for severe cases"
        ],
        "prevention": [
            "Prune out dead wood and cankers during dormancy",
            "Remove mummified fruits from trees and ground",
            "Maintain balanced fertilization — avoid excess nitrogen",
            "Protect trees from winter injury",
            "Avoid wounding trees during cultivation"
        ],
        "severity": "High — can destroy entire fruit crop and weaken tree structure"
    },
    "Apple - Cedar Apple Rust": {
        "crop": "Apple",
        "disease": "Cedar Apple Rust",
        "pathogen": "Gymnosporangium juniperi-virginianae (fungus)",
        "symptoms": "Bright yellow-orange spots on upper leaf surface. As spots mature, small raised tubes (aecia) form on the leaf underside. Fruit may develop similar orange spots.",
        "causes": "Requires two hosts — apple and cedar/juniper. Spores travel via wind from cedar galls to apple trees in spring.",
        "favorable_conditions": "Warm spring rains (13-25°C). Cedar/juniper trees within 2-3 miles. Extended wet periods during apple bloom.",
        "organic_remedies": [
            "Remove nearby cedar/juniper trees within 300 feet if possible",
            "Apply sulfur sprays during early leaf development",
            "Use neem oil as preventive during wet spring weather",
            "Improve air circulation through canopy management"
        ],
        "chemical_treatments": [
            "Myclobutanil (Systhane) at labeled rate from pink bud to 2nd cover",
            "Mancozeb 75% WP at 2.5g/L as protectant",
            "Propiconazole (Tilt) for curative action",
            "Triadimefon (Bayleton) at first sign of disease"
        ],
        "prevention": [
            "Plant rust-resistant apple varieties (Freedom, Liberty, Redfree)",
            "Remove cedar trees within proximity if feasible",
            "Begin fungicide program at green tip stage",
            "Monitor weather for spring rain events"
        ],
        "severity": "Medium — primarily cosmetic on fruit, can cause defoliation in severe cases"
    },
    "Apple - Healthy": {
        "crop": "Apple",
        "disease": "None — Healthy",
        "symptoms": "No disease symptoms detected. Plant appears healthy with normal green foliage.",
        "general_care": [
            "Maintain regular watering schedule — deep water weekly during dry spells",
            "Apply balanced fertilizer (10-10-10) in early spring",
            "Prune annually during dormancy for good air circulation",
            "Monitor regularly for early signs of pests and diseases",
            "Mulch around base to retain moisture and suppress weeds",
            "Thin fruit to improve size and prevent biennial bearing"
        ],
        "severity": "None — crop is healthy"
    },
    "Bell Pepper - Bacterial Spot": {
        "crop": "Bell Pepper",
        "disease": "Bacterial Spot",
        "pathogen": "Xanthomonas campestris pv. vesicatoria (bacterium)",
        "symptoms": "Small, water-soaked spots on leaves that become brown with yellow halos. Spots may coalesce causing leaf drop. Raised, scab-like spots on fruit surface.",
        "causes": "Bacteria survive on seed surfaces and plant debris. Spread by rain splash, overhead irrigation, and contaminated tools.",
        "favorable_conditions": "Warm, wet conditions (24-30°C). Overhead irrigation. High humidity with frequent rain.",
        "organic_remedies": [
            "Apply copper hydroxide sprays at first sign (use cautiously — phytotoxicity risk)",
            "Use Bacillus subtilis-based biofungicides",
            "Remove and destroy severely infected plants",
            "Mulch to reduce rain splash from soil"
        ],
        "chemical_treatments": [
            "Copper oxychloride 50% WP at 3g/L (preventive)",
            "Streptomycin sulfate at 500ppm for seedling treatment",
            "Mancozeb + Copper combination sprays",
            "Acibenzolar-S-methyl (Actigard) as plant defense activator"
        ],
        "prevention": [
            "Use certified disease-free seeds",
            "Hot water seed treatment (50°C for 25 minutes)",
            "Rotate crops — 2-3 year rotation away from peppers and tomatoes",
            "Use drip irrigation instead of overhead sprinklers",
            "Avoid working with plants when foliage is wet",
            "Sanitize tools between plants"
        ],
        "severity": "High — can cause significant defoliation and fruit quality loss"
    },
    "Bell Pepper - Healthy": {
        "crop": "Bell Pepper",
        "disease": "None — Healthy",
        "symptoms": "No disease symptoms detected. Plant appears healthy.",
        "general_care": [
            "Water consistently — peppers need 1-2 inches per week",
            "Apply balanced fertilizer at transplant and during fruiting",
            "Mulch to maintain soil moisture and temperature",
            "Stake or cage plants for support",
            "Monitor for aphids, whiteflies, and pepper weevils",
            "Harvest promptly when peppers reach desired color"
        ],
        "severity": "None — crop is healthy"
    },
    "Cherry - Healthy": {
        "crop": "Cherry",
        "disease": "None — Healthy",
        "symptoms": "No disease symptoms detected. Plant appears healthy.",
        "general_care": [
            "Water deeply but infrequently during dry periods",
            "Apply nitrogen fertilizer in early spring",
            "Prune in late summer to reduce disease risk",
            "Protect fruit from birds with netting",
            "Monitor for cherry fruit fly and aphids",
            "Avoid waterlogging — cherries are sensitive to wet roots"
        ],
        "severity": "None — crop is healthy"
    },
    "Cherry - Powdery Mildew": {
        "crop": "Cherry",
        "disease": "Powdery Mildew",
        "pathogen": "Podosphaera clandestina (fungus)",
        "symptoms": "White, powdery coating on leaves, shoots, and sometimes fruit. Young leaves curl and become distorted. Severe infections cause stunted growth and premature leaf drop.",
        "causes": "Fungal spores overwinter in buds and spread by wind. Unlike most fungi, does NOT require free water for infection.",
        "favorable_conditions": "Moderate temperatures (20-25°C). High humidity but dry leaf surfaces. Shaded canopy with poor air circulation.",
        "organic_remedies": [
            "Apply potassium bicarbonate solution (5g/L) as foliar spray",
            "Neem oil at 1-2% concentration",
            "Sulfur-based fungicides as preventive",
            "Milk spray (1:9 milk to water) as organic alternative",
            "Prune to improve air circulation"
        ],
        "chemical_treatments": [
            "Myclobutanil (Systhane) at labeled rate",
            "Trifloxystrobin (Flint) as preventive and curative",
            "Tebuconazole at 1ml/L for systemic control",
            "Sulfur 80% WP at 3g/L (avoid in hot weather above 30°C)"
        ],
        "prevention": [
            "Plant resistant varieties when available",
            "Maintain open canopy through proper pruning",
            "Avoid excess nitrogen fertilization",
            "Space trees adequately for air movement",
            "Monitor susceptible new growth in spring"
        ],
        "severity": "Medium — affects fruit quality and tree vigor if left unchecked"
    },
    "Corn (Maize) - Cercospora Leaf Spot": {
        "crop": "Corn (Maize)",
        "disease": "Cercospora Leaf Spot (Gray Leaf Spot)",
        "pathogen": "Cercospora zeae-maydis (fungus)",
        "symptoms": "Rectangular, gray to tan lesions running parallel to leaf veins. Lesions are sharply defined and may coalesce to blight large leaf areas. Lower leaves affected first.",
        "causes": "Fungus survives in corn residue. Spores spread by wind and rain splash. Continuous corn planting increases risk.",
        "favorable_conditions": "High humidity (>95%) and moderate temperatures (22-30°C). Prolonged dew periods. Minimum tillage with corn residue on surface.",
        "organic_remedies": [
            "Crop rotation — rotate away from corn for 1-2 years",
            "Tillage to bury infected residue",
            "Use resistant hybrids rated for gray leaf spot",
            "Apply Trichoderma-based biofungicides"
        ],
        "chemical_treatments": [
            "Azoxystrobin (Quadris) at VT-R1 timing",
            "Pyraclostrobin + Metconazole (Headline AMP)",
            "Propiconazole (Tilt) at recommended rate",
            "Trifloxystrobin at tasseling stage"
        ],
        "prevention": [
            "Plant resistant/tolerant hybrids",
            "Rotate with soybeans or other non-host crops",
            "Reduce surface residue through tillage",
            "Scout fields starting at V6 growth stage",
            "Consider fungicide when disease reaches ear leaf"
        ],
        "severity": "High — can reduce yields by 20-40% in susceptible hybrids"
    },
    "Corn (Maize) - Common Rust": {
        "crop": "Corn (Maize)",
        "disease": "Common Rust",
        "pathogen": "Puccinia sorghi (fungus)",
        "symptoms": "Small, oval to elongated, cinnamon-brown pustules on both leaf surfaces. Pustules may darken to black as the season progresses. Heavy infections cause yellowing and early leaf death.",
        "causes": "Spores blow northward from tropical regions each growing season. Cannot overwinter in temperate climates.",
        "favorable_conditions": "Cool to moderate temperatures (15-25°C). High humidity with dew. Late-planted corn is more susceptible.",
        "organic_remedies": [
            "Plant resistant hybrids with Rp genes",
            "Early planting to avoid peak spore arrival",
            "Maintain balanced nutrition for plant vigor",
            "Apply neem-based products for mild infections"
        ],
        "chemical_treatments": [
            "Azoxystrobin at early infection stage",
            "Propiconazole (Tilt) at 1ml/L",
            "Mancozeb 75% WP at 2.5g/L as protectant",
            "Tebuconazole for systemic control"
        ],
        "prevention": [
            "Select resistant hybrids",
            "Plant early to reduce exposure",
            "Scout regularly from V8 growth stage",
            "Fungicide generally only economical on sweet corn or seed corn"
        ],
        "severity": "Low to Medium — rarely causes significant yield loss in field corn"
    },
    "Corn (Maize) - Healthy": {
        "crop": "Corn (Maize)",
        "disease": "None — Healthy",
        "symptoms": "No disease symptoms detected. Plant appears healthy.",
        "general_care": [
            "Ensure adequate nitrogen at V6-V8 stage",
            "Maintain consistent moisture especially during silking",
            "Scout for corn borer and rootworm",
            "Monitor for nutrient deficiencies (yellow leaves = nitrogen, purple = phosphorus)",
            "Control weeds early in season for best yields"
        ],
        "severity": "None — crop is healthy"
    },
    "Corn (Maize) - Northern Leaf Blight": {
        "crop": "Corn (Maize)",
        "disease": "Northern Leaf Blight (NLB)",
        "pathogen": "Exserohilum turcicum (fungus)",
        "symptoms": "Long (3-15cm), elliptical, gray-green to tan lesions on leaves. Lesions may have a cigar shape. Severe infections cause extensive blighting of leaves.",
        "causes": "Fungus survives on corn debris. Spores are wind-dispersed and rain-splashed. Continuous corn increases inoculum.",
        "favorable_conditions": "Moderate temperatures (18-27°C). Heavy dew and frequent rainfall. 6+ hours of leaf wetness daily.",
        "organic_remedies": [
            "Crop rotation to reduce inoculum",
            "Deep plowing to bury infected residue",
            "Plant resistant hybrids with Ht genes",
            "Trichoderma applications to decompose residue"
        ],
        "chemical_treatments": [
            "Azoxystrobin (Quadris) at disease onset",
            "Propiconazole + Azoxystrobin combinations",
            "Mancozeb 75% WP at 2.5g/L (protective)",
            "Pyraclostrobin at VT stage for susceptible hybrids"
        ],
        "prevention": [
            "Plant hybrids with polygenic resistance",
            "Rotate crops to break disease cycle",
            "Manage residue through tillage",
            "Scout from V6 and apply fungicide if disease reaches third leaf below ear"
        ],
        "severity": "High — yield losses of 30-50% possible when upper leaves are blighted before grain fill"
    },
    "Grape - Black Rot": {
        "crop": "Grape",
        "disease": "Black Rot",
        "pathogen": "Guignardia bidwellii (fungus)",
        "symptoms": "Circular, tan spots with dark borders on leaves. Fruit develops light brown spots that quickly rot entire berry — berries shrivel into hard, black mummies.",
        "causes": "Fungus overwinters in mummified berries on vine or ground. Spores released during spring rain.",
        "favorable_conditions": "Warm, wet spring weather (21-32°C). Rain or heavy dew during bloom through veraison. Poorly maintained vineyards.",
        "organic_remedies": [
            "Remove and destroy mummified berries before bud break",
            "Apply copper-based sprays in dormant season",
            "Sulfur applications during early growth",
            "Improve canopy management for air flow"
        ],
        "chemical_treatments": [
            "Myclobutanil (Systhane) from immediate pre-bloom through 4 weeks post-bloom",
            "Mancozeb before bloom, captan after bloom",
            "Azoxystrobin for curative activity",
            "Tebuconazole at labeled rates"
        ],
        "prevention": [
            "Strict sanitation — remove all mummies",
            "Canopy management for sunlight and air",
            "Fungicide program from 10-inch shoot growth through 4-5 weeks post-bloom",
            "Choose resistant varieties where possible"
        ],
        "severity": "Very High — can destroy 80%+ of the crop in favorable conditions"
    },
    "Grape - Esca (Black Measles)": {
        "crop": "Grape",
        "disease": "Esca (Black Measles)",
        "pathogen": "Complex of fungi including Phaeomoniella chlamydospora, Phaeoacremonium spp., and Fomitiporia mediterranea",
        "symptoms": "Tiger-stripe pattern on leaves — interveinal chlorosis and necrosis. Dark spots on berries resembling measles. Chronic decline with reduced vigor. Sudden vine death possible (apoplexy).",
        "causes": "Fungi colonize the vine's vascular system through pruning wounds. Complex disease that may take years to manifest.",
        "favorable_conditions": "Water stress followed by heavy irrigation. Older vines (>8 years). Large pruning wounds. Hot climates.",
        "organic_remedies": [
            "Apply wound sealant immediately after pruning",
            "Trunk surgery — remove infected wood and apply wound protectant",
            "Trichoderma-based biocontrol agents on pruning wounds",
            "Improve vine vigor with balanced nutrition"
        ],
        "chemical_treatments": [
            "Sodium arsenite (restricted/banned in many regions)",
            "Trichoderma harzianum-based products on wounds",
            "Fosetyl-aluminum trunk injections (experimental)",
            "No fully effective chemical cure — management is key"
        ],
        "prevention": [
            "Prune in dry weather late in dormancy",
            "Make small pruning cuts and seal wounds",
            "Apply Trichoderma within 24 hours of pruning",
            "Avoid vine stress through consistent irrigation",
            "Rogue out severely infected vines"
        ],
        "severity": "Very High — chronic, incurable trunk disease that progressively kills vines"
    },
    "Grape - Healthy": {
        "crop": "Grape",
        "disease": "None — Healthy",
        "symptoms": "No disease symptoms detected. Plant appears healthy.",
        "general_care": [
            "Train and prune properly for canopy management",
            "Water deeply and less frequently — grapes prefer drier conditions",
            "Apply balanced fertilizer in early spring",
            "Monitor for powdery mildew, downy mildew, and pests",
            "Thin clusters for premium fruit quality",
            "Protect ripening fruit from birds"
        ],
        "severity": "None — crop is healthy"
    },
    "Grape - Leaf Blight": {
        "crop": "Grape",
        "disease": "Leaf Blight (Isariopsis Leaf Spot)",
        "pathogen": "Pseudocercospora vitis (fungus)",
        "symptoms": "Small, dark brown spots with yellow halos on leaves. Spots may coalesce causing large necrotic patches. Premature defoliation in severe cases.",
        "causes": "Fungus spreads via wind-borne conidia. Survives on fallen infected leaves.",
        "favorable_conditions": "Warm, humid conditions. Poor air circulation. Dense canopy.",
        "organic_remedies": [
            "Remove infected leaves and destroy",
            "Improve air circulation through canopy management",
            "Apply Bordeaux mixture (copper sulfate + lime)",
            "Use Trichoderma-based biofungicides"
        ],
        "chemical_treatments": [
            "Mancozeb 75% WP at 2.5g/L",
            "Carbendazim 50% WP at 1g/L",
            "Copper oxychloride 50% WP at 3g/L",
            "Azoxystrobin for systemic protection"
        ],
        "prevention": [
            "Maintain open canopy for air and light penetration",
            "Remove fallen leaves to reduce inoculum",
            "Apply preventive fungicides during wet periods",
            "Avoid excessive nitrogen that promotes dense growth"
        ],
        "severity": "Medium — primarily affects canopy vigor and can reduce fruit quality"
    },
    "Peach - Bacterial Spot": {
        "crop": "Peach",
        "disease": "Bacterial Spot",
        "pathogen": "Xanthomonas arboricola pv. pruni (bacterium)",
        "symptoms": "Angular, water-soaked lesions on leaves that become necrotic. Shot-hole appearance as dead tissue drops out. Fruit develops small, dark, sunken pits and cracks.",
        "causes": "Bacteria survive in cankers and leaf scars. Spread by wind-driven rain. Enters through stomata and wounds.",
        "favorable_conditions": "Warm, wet weather (25-30°C). Frequent rain or overhead irrigation. Sandy, acidic soils with low calcium.",
        "organic_remedies": [
            "Copper sprays at leaf fall and before bud break (dormant season only)",
            "Oxytetracycline (Mycoshield) during growing season where permitted",
            "Improve tree nutrition — calcium and zinc supplementation",
            "Remove severely infected shoots"
        ],
        "chemical_treatments": [
            "Copper hydroxide at dormant stage only (phytotoxic on foliage)",
            "Oxytetracycline during bloom and petal fall",
            "No highly effective in-season chemical control exists",
            "Focus on resistant varieties and cultural practices"
        ],
        "prevention": [
            "Plant resistant varieties (Contender, Madison, Redhaven)",
            "Avoid sites with poor air drainage",
            "Ensure adequate calcium in soil",
            "Use windbreaks to reduce wind-driven rain dispersal",
            "Avoid overhead irrigation"
        ],
        "severity": "High — one of the most difficult peach diseases to manage"
    },
    "Peach - Healthy": {
        "crop": "Peach",
        "disease": "None — Healthy",
        "symptoms": "No disease symptoms detected. Plant appears healthy.",
        "general_care": [
            "Prune annually in early spring for open-center shape",
            "Thin fruit to 6-8 inches apart for good size",
            "Apply dormant spray (copper + oil) before bud swell",
            "Water deeply weekly during dry periods",
            "Fertilize with 10-10-10 in early spring",
            "Monitor for peach leaf curl, brown rot, and oriental fruit moth"
        ],
        "severity": "None — crop is healthy"
    },
    "Potato - Early Blight": {
        "crop": "Potato",
        "disease": "Early Blight",
        "pathogen": "Alternaria solani (fungus)",
        "symptoms": "Dark brown to black concentric ring lesions (target spots) on older/lower leaves. Lesions have yellow halo. Tubers develop dark, sunken, leathery spots.",
        "causes": "Fungus survives in soil, infected debris, and seed tubers. Spreads by wind and rain splash. Stress-weakened plants are most susceptible.",
        "favorable_conditions": "Warm temperatures (24-29°C). Alternating wet and dry conditions. Older, stressed plants. Poor nutrition, especially low nitrogen.",
        "organic_remedies": [
            "Apply Bacillus subtilis-based biofungicides",
            "Copper-based sprays as protectant",
            "Neem oil at 2% concentration",
            "Compost tea foliar applications",
            "Mulch to reduce soil splashing"
        ],
        "chemical_treatments": [
            "Chlorothalonil (Bravo) at 2g/L as protectant",
            "Mancozeb 75% WP at 2.5g/L every 7-10 days",
            "Azoxystrobin (Quadris) for systemic control",
            "Difenoconazole (Score) at 0.5ml/L"
        ],
        "prevention": [
            "Use certified, disease-free seed potatoes",
            "Rotate crops — 3-year rotation away from potatoes and tomatoes",
            "Maintain adequate nitrogen and potassium nutrition",
            "Irrigate in morning so foliage dries quickly",
            "Remove volunteer plants and nightshade weeds",
            "Harvest carefully to avoid wounding tubers"
        ],
        "severity": "Medium to High — can reduce yield 20-50% if untreated"
    },
    "Potato - Healthy": {
        "crop": "Potato",
        "disease": "None — Healthy",
        "symptoms": "No disease symptoms detected. Plant appears healthy.",
        "general_care": [
            "Hill soil around stems as plants grow",
            "Water consistently — 1-2 inches per week",
            "Apply balanced fertilizer at planting and side-dress at hilling",
            "Monitor for Colorado potato beetle and aphids",
            "Scout regularly for early/late blight symptoms",
            "Harvest when foliage dies back naturally"
        ],
        "severity": "None — crop is healthy"
    },
    "Potato - Late Blight": {
        "crop": "Potato",
        "disease": "Late Blight",
        "pathogen": "Phytophthora infestans (oomycete)",
        "symptoms": "Large, irregular, water-soaked lesions on leaves that turn dark brown/black. White cottony mold on leaf undersides in humid conditions. Rapid plant death. Tubers develop firm, brown, granular rot.",
        "causes": "Oomycete that spreads extremely rapidly via airborne sporangia. Caused the Irish Potato Famine. Can destroy entire fields in days.",
        "favorable_conditions": "Cool, wet weather (12-20°C). Persistent moisture on leaves. Night temperatures above 10°C with humidity >90%. Rain or fog.",
        "organic_remedies": [
            "Copper-based fungicides (Bordeaux mixture) as preventive",
            "Destroy infected plants immediately by burning or deep burial",
            "Bacillus subtilis-based products for mild infections",
            "Avoid overhead irrigation",
            "Apply fixed copper sprays every 5-7 days in wet weather"
        ],
        "chemical_treatments": [
            "Metalaxyl + Mancozeb (Ridomil Gold MZ) at 2.5g/L",
            "Cymoxanil + Mancozeb (Curzate M8) as curative",
            "Chlorothalonil (Bravo) at 2g/L as protectant",
            "Dimethomorph + Mancozeb for resistant strains",
            "Mandipropamid (Revus) for modern control"
        ],
        "prevention": [
            "Use certified disease-free seed tubers",
            "Plant resistant varieties (Kennebec, Elba, Defender)",
            "Destroy all cull piles and volunteer plants",
            "Monitor regional late blight forecasting systems",
            "Apply fungicides preventively when conditions favor disease",
            "Hill tubers well to prevent spore contact with tubers",
            "Destroy foliage 2 weeks before harvest in infected fields"
        ],
        "severity": "CRITICAL — most devastating potato disease globally. Can destroy entire crop in 7-10 days."
    },
    "Strawberry - Healthy": {
        "crop": "Strawberry",
        "disease": "None — Healthy",
        "symptoms": "No disease symptoms detected. Plant appears healthy.",
        "general_care": [
            "Water at base of plants — avoid wetting foliage",
            "Mulch with straw to keep berries clean and reduce disease",
            "Remove runners to focus energy on fruit production",
            "Fertilize after harvest with balanced fertilizer",
            "Monitor for spider mites and slugs",
            "Renovate beds after harvest in June-bearing types"
        ],
        "severity": "None — crop is healthy"
    },
    "Strawberry - Leaf Scorch": {
        "crop": "Strawberry",
        "disease": "Leaf Scorch",
        "pathogen": "Diplocarpon earlianum (fungus)",
        "symptoms": "Numerous small, irregular, dark purple spots on upper leaf surface. Spots may merge causing large necrotic areas — leaves appear scorched. Severe cases cause leaf death but petioles remain green.",
        "causes": "Fungus overwinters on infected leaves. Spores dispersed by rain splash. Repeated cycles throughout growing season.",
        "favorable_conditions": "Warm, humid weather (22-30°C). Frequent rain or overhead irrigation. Dense plantings with poor air flow.",
        "organic_remedies": [
            "Remove and destroy infected leaves",
            "Improve air circulation between plants",
            "Apply compost tea or Bacillus-based biofungicides",
            "Mulch to reduce rain splash",
            "Neem oil applications at 2%"
        ],
        "chemical_treatments": [
            "Captan 50% WP at 2g/L every 10-14 days",
            "Myclobutanil (Rally) at labeled rate",
            "Azoxystrobin (Quadris) for systemic control",
            "Chlorothalonil as protectant spray"
        ],
        "prevention": [
            "Plant resistant varieties (Allstar, Earliglow)",
            "Use drip irrigation instead of overhead",
            "Maintain proper plant spacing",
            "Renovate beds after harvest — mow foliage and thin crowns",
            "Remove old infected leaves in spring before new growth"
        ],
        "severity": "Medium — reduces plant vigor and fruit quality but rarely kills plants"
    },
    "Tomato - Bacterial Spot": {
        "crop": "Tomato",
        "disease": "Bacterial Spot",
        "pathogen": "Xanthomonas vesicatoria / X. perforans (bacterium)",
        "symptoms": "Small, dark, water-soaked spots on leaves that become raised and scab-like. Leaves yellow and drop. Fruit develops small, raised, dark spots with white halos.",
        "causes": "Bacteria survive on seed, transplants, and plant debris. Spread by rain splash, wind, tools, and workers.",
        "favorable_conditions": "Warm, wet weather (24-30°C). Frequent rain. Overhead irrigation. High humidity.",
        "organic_remedies": [
            "Copper hydroxide sprays (with caution — resistance developing)",
            "Bacillus-based biofungicides (Serenade)",
            "Acibenzolar-S-methyl (Actigard) as plant defense activator",
            "Remove severely infected plants to reduce spread"
        ],
        "chemical_treatments": [
            "Copper mancozeb combinations at 7-day intervals",
            "Streptomycin for seedling production only",
            "Fixed copper + Mancozeb tank mix",
            "Kasugamycin where registered"
        ],
        "prevention": [
            "Use pathogen-free seed and transplants",
            "Hot water seed treatment (50°C for 25 minutes)",
            "3-year crop rotation away from peppers and tomatoes",
            "Use drip irrigation",
            "Avoid working with wet plants",
            "Sanitize tools and equipment"
        ],
        "severity": "High — can cause severe defoliation and unmarketable fruit"
    },
    "Tomato - Early Blight": {
        "crop": "Tomato",
        "disease": "Early Blight",
        "pathogen": "Alternaria solani (fungus)",
        "symptoms": "Dark concentric ring (target-shaped) lesions on older/lower leaves. Lesions have yellow halos. Stem lesions at soil line (collar rot). Fruit develops dark, leathery spots near stem end.",
        "causes": "Fungus persists in soil and crop residue. Spores spread by wind and rain. Stressed and nutrient-deficient plants are most vulnerable.",
        "favorable_conditions": "Warm weather (24-29°C). Alternating wet/dry periods. Heavy fruit load stressing plants. Low nitrogen or potassium.",
        "organic_remedies": [
            "Apply copper-based fungicides preventively",
            "Bacillus subtilis products (Serenade)",
            "Neem oil at 2% concentration",
            "Remove lower infected leaves promptly",
            "Mulch heavily to prevent soil splash"
        ],
        "chemical_treatments": [
            "Chlorothalonil (Bravo) at 2g/L every 7-10 days",
            "Mancozeb 75% WP at 2.5g/L",
            "Azoxystrobin for systemic protection",
            "Difenoconazole (Score) at 0.5ml/L"
        ],
        "prevention": [
            "Rotate crops — 3 year minimum",
            "Stake and prune for air circulation",
            "Water at base, never overhead",
            "Maintain adequate fertilization throughout season",
            "Remove and destroy crop debris after season",
            "Use resistant varieties where available"
        ],
        "severity": "Medium to High — progressive disease that worsens through the season"
    },
    "Tomato - Healthy": {
        "crop": "Tomato",
        "disease": "None — Healthy",
        "symptoms": "No disease symptoms detected. Plant appears healthy.",
        "general_care": [
            "Water deeply and consistently — avoid wetting foliage",
            "Stake or cage for support and air circulation",
            "Apply calcium-rich fertilizer to prevent blossom end rot",
            "Prune suckers on indeterminate varieties",
            "Monitor for hornworms, aphids, and whiteflies",
            "Mulch to retain moisture and prevent disease splash"
        ],
        "severity": "None — crop is healthy"
    },
    "Tomato - Late Blight": {
        "crop": "Tomato",
        "disease": "Late Blight",
        "pathogen": "Phytophthora infestans (oomycete)",
        "symptoms": "Large, irregular, water-soaked, greenish-black lesions on leaves. White fuzzy mold on leaf undersides. Rapid browning and collapse of foliage. Greasy-looking, firm, brown spots on fruit.",
        "causes": "Same pathogen as potato late blight. Spreads via airborne sporangia extremely rapidly. Can travel miles on wind.",
        "favorable_conditions": "Cool, wet conditions (12-22°C). Persistent leaf wetness. Night temps >10°C. Rainy or foggy weather.",
        "organic_remedies": [
            "Copper-based fungicides applied frequently (every 5-7 days)",
            "IMMEDIATELY remove and destroy all infected plants (do NOT compost)",
            "Bacillus-based products for early/mild infections only",
            "Kaolin clay applications as barrier"
        ],
        "chemical_treatments": [
            "Metalaxyl + Mancozeb (Ridomil Gold) at 2.5g/L",
            "Cymoxanil + Mancozeb for curative action",
            "Chlorothalonil as preventive in wet seasons",
            "Mandipropamid (Revus) for modern control",
            "Fluopicolide (Presidio) for resistant strains"
        ],
        "prevention": [
            "Use resistant varieties (Iron Lady, Defiant, Mountain Magic)",
            "Monitor weather forecasts and regional late blight alerts",
            "Apply preventive fungicide during cool, wet weather",
            "Avoid planting near potatoes",
            "Remove volunteer tomato and potato plants",
            "Ensure excellent air circulation"
        ],
        "severity": "CRITICAL — can destroy entire planting in days. Immediate action required."
    },
    "Tomato - Septoria Leaf Spot": {
        "crop": "Tomato",
        "disease": "Septoria Leaf Spot",
        "pathogen": "Septoria lycopersici (fungus)",
        "symptoms": "Numerous small (2-3mm), circular spots with dark brown borders and gray centers. Tiny black dots (pycnidia) visible in spot centers. Lower leaves affected first, progressing upward.",
        "causes": "Fungus survives on crop debris and solanaceous weeds. Spores spread by rain splash, tools, and workers.",
        "favorable_conditions": "Warm, wet weather (20-25°C). Frequent rain or overhead watering. High humidity. Dense plantings.",
        "organic_remedies": [
            "Remove infected lower leaves promptly",
            "Apply copper-based fungicides",
            "Bacillus-based biofungicides",
            "Mulch to prevent rain splash from soil",
            "Improve air circulation through proper staking"
        ],
        "chemical_treatments": [
            "Chlorothalonil at 2g/L every 7 days during wet weather",
            "Mancozeb 75% WP at 2.5g/L",
            "Azoxystrobin for systemic protection",
            "Difenoconazole (Score) for curative action"
        ],
        "prevention": [
            "Rotate crops — avoid planting tomatoes in same spot for 3 years",
            "Remove all crop debris at end of season",
            "Control solanaceous weeds (nightshade, horsenettle)",
            "Use drip irrigation",
            "Space plants and prune for air flow",
            "Stake plants to keep foliage off ground"
        ],
        "severity": "Medium to High — causes severe defoliation reducing yield and exposing fruit to sunscald"
    },
    "Tomato - Yellow Leaf Curl Virus": {
        "crop": "Tomato",
        "disease": "Yellow Leaf Curl Virus (TYLCV)",
        "pathogen": "Tomato Yellow Leaf Curl Virus (Begomovirus family), transmitted by whitefly (Bemisia tabaci)",
        "symptoms": "Severe upward curling and cupping of leaves. Leaves become small, crumpled, and yellow along margins. Stunted growth. Flower drop and severely reduced fruit set.",
        "causes": "Virus transmitted by silverleaf whitefly (Bemisia tabaci type B). Whiteflies acquire virus by feeding on infected plants and transmit to healthy ones.",
        "favorable_conditions": "Hot, dry weather favoring whitefly populations. Year-round warm climates. Proximity to other infected crops or weeds.",
        "organic_remedies": [
            "Remove and destroy infected plants immediately (virus has no cure)",
            "Release natural enemies — Encarsia formosa, lacewings",
            "Yellow sticky traps to monitor and reduce whitefly population",
            "Neem oil or insecticidal soap to manage whiteflies",
            "Use reflective mulches to repel whiteflies"
        ],
        "chemical_treatments": [
            "Imidacloprid (Confidor) soil drench at transplanting for whitefly control",
            "Thiamethoxam (Actara) as systemic insecticide",
            "Pyriproxyfen (juvenile hormone analog) against whitefly nymphs",
            "Spiromesifen for whitefly resistance management",
            "NOTE: No chemical can cure the virus — treatments target the whitefly vector"
        ],
        "prevention": [
            "Use TYLCV-resistant varieties (Ty genes)",
            "Cover nursery with fine insect-proof netting (50 mesh or finer)",
            "Transplant whitefly-free seedlings",
            "Remove weed hosts (Datura, Solanum spp.)",
            "Avoid planting near older infected tomato fields",
            "Remove crop residue promptly after harvest",
            "Practice crop-free period in endemic areas"
        ],
        "severity": "CRITICAL — no cure exists. Prevention and vector management are the only options. Can cause 100% yield loss."
    }
}


def get_disease_knowledge(disease_name: str) -> dict:
    """
    Retrieve knowledge base entry for a specific disease.
    Falls back to partial matching if exact key not found.
    """
    # Exact match
    if disease_name in DISEASE_KNOWLEDGE:
        return DISEASE_KNOWLEDGE[disease_name]

    # Partial match (case-insensitive)
    disease_lower = disease_name.lower()
    for key, value in DISEASE_KNOWLEDGE.items():
        if disease_lower in key.lower() or key.lower() in disease_lower:
            return value

    return {}


def get_all_diseases_for_crop(crop_name: str) -> list:
    """Get all known diseases for a specific crop."""
    results = []
    crop_lower = crop_name.lower()
    for key, value in DISEASE_KNOWLEDGE.items():
        if crop_lower in key.lower():
            results.append(value)
    return results


def build_rag_context(predicted_disease: str, crop_type: str = None) -> str:
    """
    Build RAG context string for the LLM from the knowledge base.
    Includes info about the predicted disease + related diseases for the crop.
    """
    context_parts = []

    # Primary disease knowledge
    primary_knowledge = get_disease_knowledge(predicted_disease)
    if primary_knowledge:
        context_parts.append("=== PRIMARY DISEASE KNOWLEDGE ===")
        context_parts.append(f"Disease: {primary_knowledge.get('disease', predicted_disease)}")
        context_parts.append(f"Crop: {primary_knowledge.get('crop', 'Unknown')}")
        if 'pathogen' in primary_knowledge:
            context_parts.append(f"Pathogen: {primary_knowledge['pathogen']}")
        context_parts.append(f"Symptoms: {primary_knowledge.get('symptoms', 'N/A')}")
        if 'causes' in primary_knowledge:
            context_parts.append(f"Causes: {primary_knowledge['causes']}")
        if 'favorable_conditions' in primary_knowledge:
            context_parts.append(f"Favorable Conditions: {primary_knowledge['favorable_conditions']}")
        if 'organic_remedies' in primary_knowledge:
            context_parts.append("Organic Remedies: " + "; ".join(primary_knowledge['organic_remedies']))
        if 'chemical_treatments' in primary_knowledge:
            context_parts.append("Chemical Treatments: " + "; ".join(primary_knowledge['chemical_treatments']))
        if 'prevention' in primary_knowledge:
            context_parts.append("Prevention: " + "; ".join(primary_knowledge['prevention']))
        context_parts.append(f"Severity: {primary_knowledge.get('severity', 'Unknown')}")

    # Related diseases for same crop
    if crop_type:
        related = get_all_diseases_for_crop(crop_type)
        if len(related) > 1:
            context_parts.append("\n=== OTHER KNOWN DISEASES FOR THIS CROP ===")
            for disease in related:
                name = disease.get('disease', 'Unknown')
                if name != primary_knowledge.get('disease'):
                    context_parts.append(f"- {name}: {disease.get('symptoms', 'N/A')[:100]}...")

    return "\n".join(context_parts)
