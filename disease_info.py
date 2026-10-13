"""
Disease information database for plant disease identification system.
Contains detailed treatment, prevention, and care information for all 38 PlantVillage classes.
"""

DISEASE_INFO = {
    # ── Apple ────────────────────────────────────────────────────────────────────
    "Apple___Apple_scab": {
        "severity": "moderate",
        "description": "Apple scab is a fungal disease caused by Venturia inaequalis. It creates dark, olive-green lesions on leaves and fruit, leading to premature leaf drop and reduced fruit quality.",
        "symptoms": [
            "Dark olive-green to brown velvety spots on leaves",
            "Distorted or crinkled leaf margins",
            "Scabby, corky lesions on fruit surface",
            "Premature defoliation in severe cases",
        ],
        "treatment": [
            "Apply fungicides (captan, myclobutanil) during spring",
            "Remove and destroy fallen infected leaves",
            "Prune trees for better air circulation",
            "Apply sulfur or copper-based sprays preventively",
        ],
        "prevention": [
            "Plant scab-resistant apple varieties (e.g., Liberty, Enterprise)",
            "Maintain proper tree spacing for airflow",
            "Apply dormant oil spray before bud break",
            "Keep orchard floor clean of debris",
        ],
    },
    "Apple___Black_rot": {
        "severity": "high",
        "description": "Black rot is caused by Botryosphaeria obtusa. It attacks fruit, leaves, and bark, causing significant losses. Fruit develops expanding brown lesions that eventually turn the entire fruit black.",
        "symptoms": [
            "Frogeye leaf spots — circular brown lesions with purple borders",
            "Expanding brown rot on fruit starting from calyx end",
            "Mummified fruit remaining on tree",
            "Cankers on limbs and trunk bark",
        ],
        "treatment": [
            "Remove mummified fruit and cankered branches",
            "Apply captan or thiophanate-methyl fungicides",
            "Prune infected limbs 15 cm below visible canker",
            "Dispose of pruned material away from orchard",
        ],
        "prevention": [
            "Remove all mummified fruit before spring",
            "Maintain tree vigor with proper fertilization",
            "Avoid wounding trees during cultivation",
            "Apply preventive fungicide at petal fall",
        ],
    },
    "Apple___Cedar_apple_rust": {
        "severity": "moderate",
        "description": "Cedar apple rust is caused by Gymnosporangium juniperi-virginianae. It requires both cedar (juniper) and apple trees to complete its life cycle, producing bright orange-yellow spots on apple leaves.",
        "symptoms": [
            "Bright yellow-orange spots on upper leaf surface",
            "Tube-like structures (aecia) on undersides of leaves",
            "Spots may appear on fruit and young twigs",
            "Early defoliation in severe infections",
        ],
        "treatment": [
            "Apply myclobutanil or mancozeb fungicides at bloom",
            "Remove nearby cedar/juniper trees within 300m if possible",
            "Destroy cedar galls before they produce spores in spring",
            "Apply 2-3 fungicide sprays from pink bud through petal fall",
        ],
        "prevention": [
            "Plant rust-resistant apple varieties",
            "Remove all eastern red cedar and juniper within 2 miles",
            "Scout for cedar galls in winter and remove them",
            "Maintain a preventive spray schedule",
        ],
    },
    "Apple___healthy": {
        "severity": "none",
        "description": "This apple leaf shows no signs of disease. The plant appears healthy with normal green coloration and no visible lesions or abnormalities.",
        "symptoms": [],
        "treatment": [
            "No treatment needed — continue regular care",
            "Maintain balanced fertilization schedule",
            "Monitor regularly for early signs of disease",
        ],
        "prevention": [
            "Continue proper watering and nutrition program",
            "Maintain good air circulation through pruning",
            "Apply dormant sprays in late winter",
            "Scout weekly during growing season",
        ],
    },

    # ── Blueberry ────────────────────────────────────────────────────────────────
    "Blueberry___healthy": {
        "severity": "none",
        "description": "This blueberry leaf appears healthy with no signs of disease. Normal green coloration and intact leaf structure observed.",
        "symptoms": [],
        "treatment": [
            "No treatment needed — continue regular care",
            "Maintain acidic soil pH (4.5–5.5)",
        ],
        "prevention": [
            "Use pine bark mulch to maintain soil acidity",
            "Ensure consistent watering, especially during fruiting",
            "Prune old canes annually to stimulate new growth",
            "Apply appropriate acidifying fertilizer",
        ],
    },

    # ── Cherry ───────────────────────────────────────────────────────────────────
    "Cherry_(including_sour)___Powdery_mildew": {
        "severity": "moderate",
        "description": "Powdery mildew on cherry is caused by Podosphaera clandestina. It creates a white powdery coating on leaves, shoots, and fruit, reducing photosynthesis and fruit quality.",
        "symptoms": [
            "White, powdery fungal growth on leaf surfaces",
            "Leaf curling and distortion",
            "Stunted shoot growth",
            "Reduced fruit set and quality",
        ],
        "treatment": [
            "Apply sulfur-based or potassium bicarbonate fungicides",
            "Use myclobutanil or trifloxystrobin at first signs",
            "Remove and destroy heavily infected shoots",
            "Improve air circulation by selective pruning",
        ],
        "prevention": [
            "Select resistant varieties when available",
            "Avoid excessive nitrogen fertilization",
            "Space trees adequately for air movement",
            "Apply preventive fungicide before symptoms appear",
        ],
    },
    "Cherry_(including_sour)___healthy": {
        "severity": "none",
        "description": "This cherry leaf appears healthy with no disease symptoms visible. Good green coloration and normal leaf structure.",
        "symptoms": [],
        "treatment": [
            "No treatment needed — continue regular care",
            "Maintain proper watering schedule",
        ],
        "prevention": [
            "Monitor for early signs of powdery mildew",
            "Maintain tree vigor with balanced fertilization",
            "Ensure proper drainage around root zone",
            "Prune for open canopy structure",
        ],
    },

    # ── Corn ─────────────────────────────────────────────────────────────────────
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "severity": "high",
        "description": "Gray leaf spot is caused by Cercospora zeae-maydis. It creates rectangular grayish-tan lesions that follow leaf veins and can significantly reduce yield by destroying photosynthetic area.",
        "symptoms": [
            "Rectangular gray-tan lesions bounded by leaf veins",
            "Lesions up to 5cm long, 2-3mm wide",
            "Lower leaves affected first, progressing upward",
            "Severe cases: entire leaf turns gray-brown",
        ],
        "treatment": [
            "Apply strobilurin or triazole fungicides at VT-R1 stage",
            "Rotate crops to non-host species (soybean, wheat)",
            "Remove crop residue after harvest by tillage",
            "Apply foliar fungicide when disease reaches ear leaf",
        ],
        "prevention": [
            "Plant resistant or tolerant corn hybrids",
            "Rotate to non-corn crops for 1-2 years",
            "Reduce surface residue through tillage",
            "Avoid continuous corn in humid fields",
        ],
    },
    "Corn_(maize)___Common_rust_": {
        "severity": "moderate",
        "description": "Common rust is caused by Puccinia sorghi. It produces small, circular to elongated reddish-brown pustules on both leaf surfaces. Usually a minor disease but can be severe on susceptible hybrids.",
        "symptoms": [
            "Small circular to elongated cinnamon-brown pustules",
            "Pustules on both upper and lower leaf surfaces",
            "Powdery reddish-brown spores released when pustules rupture",
            "Yellowing and death of heavily infected leaves",
        ],
        "treatment": [
            "Apply triazole or strobilurin fungicides if severe",
            "Generally no treatment needed for moderate infections",
            "Scout fields and treat if pustules cover >50% of leaf area",
            "Fungicide most effective before tasseling",
        ],
        "prevention": [
            "Plant rust-resistant corn hybrids",
            "Early planting to avoid peak spore periods",
            "Monitor weather for conditions favoring rust (cool, humid)",
            "Scout fields regularly starting at V8 stage",
        ],
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "severity": "high",
        "description": "Northern leaf blight (NLB) is caused by Exserohilum turcicum. It produces large cigar-shaped grayish-green to tan lesions that can coalesce and destroy significant leaf area.",
        "symptoms": [
            "Large cigar-shaped (3-15 cm) gray-green lesions",
            "Lesions start on lower leaves and move up",
            "Tan to gray sporulation in lesion centers",
            "Severe cases: leaves die from tip backward",
        ],
        "treatment": [
            "Apply foliar fungicides (azoxystrobin, pyraclostrobin) at VT-R1",
            "Rotate to non-host crops for at least one season",
            "Remove or bury crop residue after harvest",
            "Apply fungicide when disease found on 3rd leaf below ear",
        ],
        "prevention": [
            "Plant NLB-resistant hybrids with Ht genes",
            "Rotate crops to break disease cycle",
            "Manage crop residue to reduce inoculum",
            "Avoid planting late into heavy NLB fields",
        ],
    },
    "Corn_(maize)___healthy": {
        "severity": "none",
        "description": "This corn leaf appears healthy with no visible disease symptoms. Normal green coloration and intact leaf structure.",
        "symptoms": [],
        "treatment": [
            "No treatment needed — continue regular management",
            "Maintain proper nitrogen and water supply",
        ],
        "prevention": [
            "Continue scouting for disease and pest issues",
            "Maintain balanced fertilization program",
            "Ensure adequate plant spacing for air circulation",
            "Rotate crops annually",
        ],
    },

    # ── Grape ────────────────────────────────────────────────────────────────────
    "Grape___Black_rot": {
        "severity": "high",
        "description": "Black rot is caused by Guignardia bidwellii. It causes circular reddish-brown leaf spots and devastating fruit rot that turns berries into hard, black shriveled mummies.",
        "symptoms": [
            "Circular tan spots with dark borders on leaves",
            "Small black pycnidia dots within leaf spots",
            "Brown soft rot starting on berries, then hardening",
            "Berries become black shriveled mummies",
        ],
        "treatment": [
            "Apply myclobutanil or mancozeb before and after bloom",
            "Remove mummified fruit and infected canes",
            "Time fungicide applications from bud break through veraison",
            "Use captan + myclobutanil rotation for resistance management",
        ],
        "prevention": [
            "Remove all mummies from vines and ground in winter",
            "Maintain open canopy for good air circulation",
            "Begin protective sprays at 10-inch shoot growth",
            "Select resistant cultivars when possible",
        ],
    },
    "Grape___Esca_(Black_Measles)": {
        "severity": "high",
        "description": "Esca (Black Measles) is a complex trunk disease caused by multiple fungi including Phaeomoniella chlamydospora and Phaeoacremonium spp. It causes distinctive interveinal striping on leaves.",
        "symptoms": [
            "Tiger-stripe pattern between leaf veins",
            "Interveinal chlorosis and necrosis",
            "Dark spots on berry skin (measles)",
            "Sudden vine collapse (apoplexy) in severe cases",
        ],
        "treatment": [
            "No curative treatment available — manage symptoms",
            "Retrain trunks from suckers below disease zone",
            "Apply wound protectants after pruning",
            "Remove and burn severely affected vines",
        ],
        "prevention": [
            "Delay pruning until late in dormant season",
            "Apply wound protectants (Trichoderma-based) after pruning",
            "Use certified disease-free planting stock",
            "Avoid large pruning wounds",
        ],
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "severity": "moderate",
        "description": "Isariopsis leaf spot (Pseudocercospora vitis) causes irregular brownish spots on grape leaves. It typically appears in warm, humid conditions.",
        "symptoms": [
            "Irregular brown to dark brown spots on leaves",
            "Spots may coalesce creating larger necrotic areas",
            "Premature defoliation in severe cases",
            "Dark sporulation visible on leaf undersides",
        ],
        "treatment": [
            "Apply copper-based fungicides early in the season",
            "Remove and destroy infected leaves",
            "Improve canopy management for air circulation",
            "Apply mancozeb or copper hydroxide at 10-14 day intervals",
        ],
        "prevention": [
            "Maintain proper vine spacing and trellising",
            "Prune for open canopy structure",
            "Remove leaf debris from vineyard floor",
            "Start preventive sprays in humid weather",
        ],
    },
    "Grape___healthy": {
        "severity": "none",
        "description": "This grape leaf appears healthy with no visible disease symptoms. Normal green coloration and intact structure.",
        "symptoms": [],
        "treatment": [
            "No treatment needed — continue standard vineyard care",
        ],
        "prevention": [
            "Maintain preventive spray schedule during growing season",
            "Monitor for early signs of fungal disease",
            "Continue proper canopy management",
            "Remove excess shoots for good air circulation",
        ],
    },

    # ── Orange ───────────────────────────────────────────────────────────────────
    "Orange___Haunglongbing_(Citrus_greening)": {
        "severity": "critical",
        "description": "Huanglongbing (HLB/Citrus greening) is caused by Candidatus Liberibacter and spread by the Asian citrus psyllid. It is one of the most devastating citrus diseases worldwide with no cure.",
        "symptoms": [
            "Asymmetric blotchy mottling/yellowing on leaves",
            "Small, lopsided, bitter-tasting fruit",
            "Fruit remains partially green even when ripe",
            "Twig dieback and overall tree decline",
        ],
        "treatment": [
            "No cure exists — manage to extend tree productivity",
            "Control psyllid vectors with systemic insecticides",
            "Apply enhanced nutrition programs (micronutrients)",
            "Remove severely symptomatic trees to reduce spread",
        ],
        "prevention": [
            "Plant certified disease-free nursery stock",
            "Control Asian citrus psyllid populations aggressively",
            "Scout regularly and remove symptomatic trees early",
            "Use protective screen in nurseries",
        ],
    },

    # ── Peach ────────────────────────────────────────────────────────────────────
    "Peach___Bacterial_spot": {
        "severity": "moderate",
        "description": "Bacterial spot is caused by Xanthomonas arboricola pv. pruni. It affects leaves, fruit, and twigs, creating angular water-soaked lesions and pitted fruit.",
        "symptoms": [
            "Small angular water-soaked spots on leaves",
            "Spots turn brown/purple with yellow halos",
            "Shot-hole appearance as dead tissue falls out",
            "Sunken, cracked, pitted lesions on fruit",
        ],
        "treatment": [
            "Apply copper sprays at leaf fall and dormant season",
            "Use oxytetracycline (Mycoshield) during growing season",
            "Improve air circulation through proper pruning",
            "Avoid overhead irrigation",
        ],
        "prevention": [
            "Plant resistant peach cultivars",
            "Apply dormant copper spray before bud break",
            "Avoid sites with poor air drainage",
            "Remove infected fallen leaves and fruit",
        ],
    },
    "Peach___healthy": {
        "severity": "none",
        "description": "This peach leaf appears healthy with no visible disease symptoms.",
        "symptoms": [],
        "treatment": ["No treatment needed — continue regular care"],
        "prevention": [
            "Apply dormant copper spray annually",
            "Monitor for signs of leaf curl and bacterial spot",
            "Maintain proper tree nutrition and watering",
        ],
    },

    # ── Pepper ───────────────────────────────────────────────────────────────────
    "Pepper,_bell___Bacterial_spot": {
        "severity": "moderate",
        "description": "Bacterial spot on pepper is caused by Xanthomonas species. It creates water-soaked spots on leaves, stems, and fruit, leading to defoliation and sunscalded fruit.",
        "symptoms": [
            "Small water-soaked spots on leaves",
            "Spots enlarge and turn brown with yellow margins",
            "Raised, scab-like lesions on fruit",
            "Severe defoliation exposing fruit to sunscald",
        ],
        "treatment": [
            "Apply copper-based bactericides with mancozeb",
            "Remove and destroy infected plant debris",
            "Avoid working in fields when plants are wet",
            "Use drip irrigation instead of overhead sprinklers",
        ],
        "prevention": [
            "Use pathogen-free certified seed and transplants",
            "Rotate crops — avoid peppers/tomatoes for 2-3 years",
            "Apply preventive copper sprays before symptom onset",
            "Maintain proper plant spacing",
        ],
    },
    "Pepper,_bell___healthy": {
        "severity": "none",
        "description": "This bell pepper leaf appears healthy with no disease symptoms visible.",
        "symptoms": [],
        "treatment": ["No treatment needed — continue regular care"],
        "prevention": [
            "Continue crop rotation practices",
            "Monitor for signs of bacterial spot regularly",
            "Maintain consistent watering schedule",
            "Apply balanced fertilizer as needed",
        ],
    },

    # ── Potato ───────────────────────────────────────────────────────────────────
    "Potato___Early_blight": {
        "severity": "moderate",
        "description": "Early blight is caused by Alternaria solani. It produces characteristic concentric-ring 'target' spots on lower leaves and can cause significant yield reduction.",
        "symptoms": [
            "Dark concentric-ring (target/bullseye) lesions on leaves",
            "Lower/older leaves affected first",
            "Yellowing around lesions, premature defoliation",
            "Dark sunken lesions on tubers",
        ],
        "treatment": [
            "Apply chlorothalonil or mancozeb at first symptoms",
            "Rotate fungicide modes of action to prevent resistance",
            "Remove and destroy infected plant debris",
            "Apply azoxystrobin alternating with protectants",
        ],
        "prevention": [
            "Plant certified disease-free seed potatoes",
            "Rotate crops (3+ years away from Solanaceae)",
            "Maintain adequate potassium and nitrogen nutrition",
            "Avoid overhead irrigation; use drip if possible",
        ],
    },
    "Potato___Late_blight": {
        "severity": "critical",
        "description": "Late blight, caused by Phytophthora infestans (the Irish Potato Famine pathogen), is one of the most devastating plant diseases. It spreads rapidly under cool, wet conditions.",
        "symptoms": [
            "Water-soaked gray-green spots on leaves",
            "White fuzzy mold on leaf undersides in humid conditions",
            "Rapid browning and blackening of foliage",
            "Firm, reddish-brown granular rot in tubers",
        ],
        "treatment": [
            "Apply systemic fungicides (metalaxyl) immediately",
            "Use protectant fungicides (chlorothalonil, mancozeb)",
            "Destroy all infected plant material (do not compost)",
            "Hill tubers to prevent spore wash into soil",
        ],
        "prevention": [
            "Use certified late-blight-free seed potatoes",
            "Plant resistant varieties (e.g., Defender, Elba)",
            "Destroy volunteer plants and cull piles",
            "Monitor weather forecasts for blight-favorable conditions",
        ],
    },
    "Potato___healthy": {
        "severity": "none",
        "description": "This potato leaf appears healthy with no visible disease symptoms.",
        "symptoms": [],
        "treatment": ["No treatment needed — continue regular care"],
        "prevention": [
            "Maintain a preventive fungicide program",
            "Scout regularly, especially under humid conditions",
            "Practice crop rotation with non-Solanaceae crops",
            "Ensure proper hilling of tubers",
        ],
    },

    # ── Raspberry ────────────────────────────────────────────────────────────────
    "Raspberry___healthy": {
        "severity": "none",
        "description": "This raspberry leaf appears healthy with no visible disease symptoms.",
        "symptoms": [],
        "treatment": ["No treatment needed — continue regular care"],
        "prevention": [
            "Maintain good air circulation between canes",
            "Remove old fruiting canes after harvest",
            "Apply dormant copper spray in early spring",
            "Avoid overhead watering",
        ],
    },

    # ── Soybean ──────────────────────────────────────────────────────────────────
    "Soybean___healthy": {
        "severity": "none",
        "description": "This soybean leaf appears healthy with no visible disease symptoms.",
        "symptoms": [],
        "treatment": ["No treatment needed — continue regular management"],
        "prevention": [
            "Practice crop rotation with corn or wheat",
            "Scout for soybean rust and other diseases",
            "Use disease-resistant varieties",
            "Maintain proper plant population and row spacing",
        ],
    },

    # ── Squash ───────────────────────────────────────────────────────────────────
    "Squash___Powdery_mildew": {
        "severity": "moderate",
        "description": "Powdery mildew on squash is caused by Erysiphe cichoracearum and Podosphaera xanthii. It creates white powdery growth on leaves, reducing photosynthesis and yield.",
        "symptoms": [
            "White powdery spots on upper leaf surfaces",
            "Spots expand to cover entire leaves",
            "Leaves turn yellow and dry out",
            "Reduced fruit size and quality",
        ],
        "treatment": [
            "Apply potassium bicarbonate or neem oil sprays",
            "Use sulfur-based fungicides (avoid above 90°F)",
            "Apply myclobutanil or trifloxystrobin for severe cases",
            "Remove and destroy heavily infected leaves",
        ],
        "prevention": [
            "Plant resistant squash varieties",
            "Provide adequate plant spacing for air movement",
            "Avoid excessive nitrogen fertilization",
            "Water at base of plant, not overhead",
        ],
    },

    # ── Strawberry ───────────────────────────────────────────────────────────────
    "Strawberry___Leaf_scorch": {
        "severity": "moderate",
        "description": "Leaf scorch is caused by Diplocarpon earlianum. It produces irregular purple spots that merge, giving leaves a scorched appearance.",
        "symptoms": [
            "Small irregular dark purple spots on leaves",
            "Spots merge, causing a burned/scorched appearance",
            "Leaf margins curl upward",
            "Reduced plant vigor and fruit production",
        ],
        "treatment": [
            "Apply captan or myclobutanil fungicides",
            "Remove and destroy infected leaves",
            "Renovate beds after harvest (mow, thin, fertilize)",
            "Apply fungicide at bloom and post-harvest",
        ],
        "prevention": [
            "Plant resistant strawberry cultivars",
            "Maintain proper plant spacing for air circulation",
            "Use drip irrigation instead of overhead sprinklers",
            "Remove old leaves during bed renovation",
        ],
    },
    "Strawberry___healthy": {
        "severity": "none",
        "description": "This strawberry leaf appears healthy with no visible disease symptoms.",
        "symptoms": [],
        "treatment": ["No treatment needed — continue regular care"],
        "prevention": [
            "Renovate beds annually after harvest",
            "Maintain proper plant spacing",
            "Use straw mulch to prevent splash-borne disease",
            "Scout regularly for leaf diseases",
        ],
    },

    # ── Tomato ───────────────────────────────────────────────────────────────────
    "Tomato___Bacterial_spot": {
        "severity": "moderate",
        "description": "Bacterial spot on tomato is caused by multiple Xanthomonas species. It creates small water-soaked spots on leaves, stems, and fruit.",
        "symptoms": [
            "Small water-soaked spots on leaves that turn brown",
            "Spots may have yellow halos",
            "Raised scab-like lesions on fruit",
            "Severe defoliation leading to sunscalded fruit",
        ],
        "treatment": [
            "Apply copper + mancozeb tank mix at first signs",
            "Remove severely infected plants",
            "Avoid working in wet fields",
            "Use bacteriophage products where available",
        ],
        "prevention": [
            "Use certified disease-free seed",
            "Practice 2-3 year crop rotation away from Solanaceae",
            "Disinfect tools and stakes between uses",
            "Use drip irrigation, not overhead",
        ],
    },
    "Tomato___Early_blight": {
        "severity": "moderate",
        "description": "Tomato early blight is caused by Alternaria solani. It causes concentric-ring (target) spots on older leaves and can lead to significant defoliation.",
        "symptoms": [
            "Concentric-ring 'target spot' lesions on older leaves",
            "Dark cankers at stem base (collar rot)",
            "Yellowing and premature drop of lower leaves",
            "Dark leathery spots on fruit near stem end",
        ],
        "treatment": [
            "Apply chlorothalonil or mancozeb fungicides",
            "Remove infected lower leaves promptly",
            "Stake plants to improve air circulation",
            "Mulch around plants to prevent soil splash",
        ],
        "prevention": [
            "Use resistant or tolerant tomato varieties",
            "Rotate crops for 3+ years",
            "Mulch to prevent rain splash from soil",
            "Ensure proper spacing between plants",
        ],
    },
    "Tomato___Late_blight": {
        "severity": "critical",
        "description": "Late blight on tomato is caused by Phytophthora infestans. It spreads rapidly in cool, wet weather and can destroy entire fields within days.",
        "symptoms": [
            "Large water-soaked grayish-green spots on leaves",
            "White fuzzy sporulation on leaf undersides",
            "Stems develop dark brown-black lesions",
            "Firm, dark, greasy rot on fruit",
        ],
        "treatment": [
            "Apply systemic fungicides (metalaxyl-M) immediately",
            "Use protectant fungicides (chlorothalonil, copper)",
            "Remove and destroy all infected plants immediately",
            "Do not compost infected material",
        ],
        "prevention": [
            "Use late-blight-resistant varieties (e.g., Mountain Magic)",
            "Monitor forecasts for blight-favorable weather",
            "Destroy volunteer potato and tomato plants",
            "Avoid overhead irrigation",
        ],
    },
    "Tomato___Leaf_Mold": {
        "severity": "moderate",
        "description": "Leaf mold is caused by Passalora fulva (formerly Cladosporium fulvum). It is mainly a greenhouse disease, thriving in high humidity and poor ventilation.",
        "symptoms": [
            "Pale green to yellowish spots on upper leaf surface",
            "Olive-green to grayish-purple velvety mold underneath",
            "Leaves curl, wither, and drop prematurely",
            "Rarely affects fruit or stems",
        ],
        "treatment": [
            "Improve greenhouse ventilation immediately",
            "Apply chlorothalonil or copper-based fungicides",
            "Reduce humidity below 85% using fans/vents",
            "Remove infected leaves and destroy them",
        ],
        "prevention": [
            "Maintain greenhouse humidity below 85%",
            "Ensure good air circulation with fans",
            "Use resistant tomato varieties (Cf genes)",
            "Avoid leaf wetness and overhead watering",
        ],
    },
    "Tomato___Septoria_leaf_spot": {
        "severity": "moderate",
        "description": "Septoria leaf spot is caused by Septoria lycopersici. It produces small circular spots with dark borders and gray centers, typically starting on lower leaves.",
        "symptoms": [
            "Small (1-3mm) circular spots with dark brown margins",
            "Gray or tan centers with tiny black specks (pycnidia)",
            "Lower leaves affected first, progressing upward",
            "Severe defoliation exposing fruit to sunscald",
        ],
        "treatment": [
            "Apply chlorothalonil or mancozeb at first symptoms",
            "Remove and destroy infected lower leaves",
            "Maintain 7-10 day spray interval in wet weather",
            "Apply copper-based products as organic alternative",
        ],
        "prevention": [
            "Rotate crops for at least 3 years",
            "Mulch to prevent soil splash onto lower leaves",
            "Stake or cage plants for better air flow",
            "Remove all tomato debris at end of season",
        ],
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "severity": "moderate",
        "description": "Two-spotted spider mites (Tetranychus urticae) are tiny arachnids that feed on plant cell contents, causing stippling, yellowing, and webbing on tomato leaves.",
        "symptoms": [
            "Fine stippling (tiny yellow dots) on upper leaf surfaces",
            "Fine webbing between leaves and stems",
            "Leaves turn bronze, then brown and crispy",
            "Tiny moving dots visible with magnification",
        ],
        "treatment": [
            "Apply insecticidal soap or neem oil spray",
            "Use miticides (abamectin, spiromesifen) for severe cases",
            "Release predatory mites (Phytoseiulus persimilis)",
            "Spray undersides of leaves thoroughly with water jets",
        ],
        "prevention": [
            "Monitor regularly with hand lens, especially in hot weather",
            "Maintain adequate plant hydration (stressed plants are susceptible)",
            "Avoid broad-spectrum insecticides that kill natural predators",
            "Keep surrounding areas free of weedy hosts",
        ],
    },
    "Tomato___Target_Spot": {
        "severity": "moderate",
        "description": "Target spot is caused by Corynespora cassiicola. It produces circular to angular spots with concentric rings on leaves, stems, and fruit.",
        "symptoms": [
            "Small brown spots with concentric rings on leaves",
            "Spots enlarge and may have yellow halos",
            "Lesions on stems and fruit",
            "Premature defoliation in severe infections",
        ],
        "treatment": [
            "Apply chlorothalonil or azoxystrobin fungicides",
            "Remove and destroy infected plant material",
            "Improve air circulation by pruning lower leaves",
            "Apply fungicides on 7-14 day schedule in wet weather",
        ],
        "prevention": [
            "Rotate crops for 2-3 years",
            "Use mulch to prevent rain splash",
            "Maintain proper plant spacing",
            "Remove crop residue after season end",
        ],
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "severity": "critical",
        "description": "TYLCV is a devastating viral disease transmitted by whiteflies (Bemisia tabaci). Infected plants are severely stunted with curled, yellowed leaves and dramatically reduced fruit set.",
        "symptoms": [
            "Severe upward leaf curling and cupping",
            "Intense yellowing of leaf margins",
            "Stunted, bushy plant growth",
            "Drastically reduced or absent fruit production",
        ],
        "treatment": [
            "No cure for virus — remove and destroy infected plants",
            "Control whitefly vectors with imidacloprid or spiromesifen",
            "Use reflective mulches to repel whiteflies",
            "Apply neem oil for mild infestations",
        ],
        "prevention": [
            "Plant TYLCV-resistant tomato varieties",
            "Use UV-reflective mulch to repel whiteflies",
            "Install fine-mesh insect screens in greenhouses",
            "Remove infected plants immediately to prevent spread",
        ],
    },
    "Tomato___Tomato_mosaic_virus": {
        "severity": "high",
        "description": "Tomato mosaic virus (ToMV) causes mottled light and dark green patterns on leaves. It is extremely stable and easily transmitted through mechanical contact.",
        "symptoms": [
            "Light/dark green mosaic pattern on leaves",
            "Leaf distortion and fern-leaf appearance",
            "Stunted plant growth",
            "Uneven fruit ripening with internal browning",
        ],
        "treatment": [
            "No cure for virus — remove infected plants immediately",
            "Disinfect tools with 10% bleach between plants",
            "Wash hands with soap before handling healthy plants",
            "Do not compost infected plant material",
        ],
        "prevention": [
            "Plant TMV/ToMV-resistant varieties (Tm-2 gene)",
            "Use certified virus-free seed",
            "Disinfect all tools, stakes, and surfaces",
            "Do not smoke or handle tobacco near tomato plants",
        ],
    },
    "Tomato___healthy": {
        "severity": "none",
        "description": "This tomato leaf appears healthy with no visible disease symptoms. Good green coloration and normal structure.",
        "symptoms": [],
        "treatment": [
            "No treatment needed — continue regular care",
            "Maintain consistent watering schedule",
        ],
        "prevention": [
            "Continue scouting for disease and pest issues weekly",
            "Maintain proper plant nutrition",
            "Ensure good air circulation through pruning",
            "Practice crop rotation annually",
        ],
    },
}

# Severity color/icon mapping
SEVERITY_MAP = {
    "none":     {"color": "#10b981", "bg": "rgba(16,185,129,0.12)", "border": "rgba(16,185,129,0.3)", "icon": "✅", "label": "Healthy"},
    "moderate": {"color": "#f59e0b", "bg": "rgba(245,158,11,0.12)",  "border": "rgba(245,158,11,0.3)", "icon": "⚠️", "label": "Moderate"},
    "high":     {"color": "#ef4444", "bg": "rgba(239,68,68,0.12)",   "border": "rgba(239,68,68,0.3)",  "icon": "🔴", "label": "High"},
    "critical": {"color": "#dc2626", "bg": "rgba(220,38,38,0.15)",   "border": "rgba(220,38,38,0.4)",  "icon": "🚨", "label": "Critical"},
}
