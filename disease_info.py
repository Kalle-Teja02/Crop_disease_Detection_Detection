# Disease information dictionary with comprehensive details
disease_data = {
    'Tomato___Bacterial_spot': {
        'name': 'Tomato - Bacterial Spot',
        'symptoms': 'Small dark brown to black spots on leaves (1-3mm), yellowing around spots, defoliation in severe cases, spots may have yellow halos, affects leaves, stems, and fruits',
        'causes': 'Caused by Xanthomonas bacteria, spreads through water splash, contaminated seeds, infected plant debris, warm humid conditions (75-86°F), overhead irrigation',
        'treatment': 'Remove and destroy infected leaves immediately, apply copper-based bactericides (Kocide, Copper hydroxide), use streptomycin sprays in early stages, improve air circulation',
        'prevention': 'Use disease-free certified seeds, avoid overhead watering, practice crop rotation (3-4 years), maintain proper plant spacing, remove plant debris, disinfect tools regularly',
        'pesticides': 'Copper hydroxide (Kocide 3000), Copper sulfate, Streptomycin sulfate, Mancozeb + Copper, Apply every 7-10 days during wet weather',
        'organic_solutions': 'Neem oil spray (2-3%), Copper soap fungicide, Bacillus subtilis biofungicide, Garlic extract spray, Maintain soil health with compost'
    },
    'Tomato___Early_blight': {
        'name': 'Tomato - Early Blight',
        'symptoms': 'Dark brown spots with concentric rings (target-like pattern) on older leaves, yellowing and dropping of lower leaves, lesions on stems and fruits, leaves curl and die',
        'causes': 'Caused by Alternaria solani fungus, favored by warm temperatures (75-85°F), high humidity, wet foliage, poor air circulation, stressed plants',
        'treatment': 'Remove infected lower leaves, apply fungicides containing chlorothalonil or mancozeb, use copper-based fungicides, ensure proper plant nutrition',
        'prevention': 'Mulch around plants to prevent soil splash, water at base of plants, stake plants for air circulation, practice 3-year crop rotation, use resistant varieties',
        'pesticides': 'Chlorothalonil (Daconil), Mancozeb (Dithane), Azoxystrobin (Quadris), Copper fungicides, Apply every 7-14 days preventively',
        'organic_solutions': 'Baking soda spray (1 tbsp per gallon), Compost tea foliar spray, Copper fungicide, Sulfur dust, Remove affected leaves promptly'
    },
    'Tomato___Late_blight': {
        'name': 'Tomato - Late Blight',
        'symptoms': 'Large brown water-soaked blotches on leaves, white fuzzy mold on undersides, rapid plant death (within days), affects stems and fruits, foul odor from infected tissue',
        'causes': 'Caused by Phytophthora infestans (same as potato blight), spreads rapidly in cool wet weather (60-70°F), high humidity, wind-borne spores, infected tubers',
        'treatment': 'Remove and destroy infected plants immediately, apply fungicides with chlorothalonil or mancozeb, do not compost infected material, act quickly as disease spreads fast',
        'prevention': 'Plant resistant varieties, ensure good drainage, avoid overhead irrigation, space plants properly, monitor weather conditions, remove volunteer plants',
        'pesticides': 'Chlorothalonil (Bravo), Mancozeb + Copper, Metalaxyl (Ridomil), Cymoxanil (Curzate), Apply preventively before symptoms appear',
        'organic_solutions': 'Copper fungicide (apply early), Destroy infected plants, Improve air circulation, Avoid working with wet plants, Use disease-free transplants'
    },
    'Tomato___Leaf_Mold': {
        'name': 'Tomato - Leaf Mold',
        'symptoms': 'Pale green or yellowish spots on upper leaf surface, olive-green to brown fuzzy mold on lower surface, leaves curl and die, reduced fruit production',
        'causes': 'Caused by Passalora fulva fungus, thrives in high humidity (>85%), poor air circulation, temperatures 70-80°F, common in greenhouses and humid climates',
        'treatment': 'Remove infected leaves, reduce humidity below 85%, improve ventilation, apply fungicides with chlorothalonil or copper, increase plant spacing',
        'prevention': 'Use resistant varieties (many F1 hybrids), ensure good air circulation, avoid overhead watering, maintain humidity below 85%, prune lower leaves',
        'pesticides': 'Chlorothalonil (Daconil), Copper fungicides, Mancozeb, Azoxystrobin, Apply when conditions favor disease',
        'organic_solutions': 'Improve greenhouse ventilation, Reduce humidity with fans, Sulfur fungicide, Neem oil spray, Baking soda solution, Remove affected leaves'
    },
    'Tomato___healthy': {
        'name': 'Healthy Tomato Plant',
        'symptoms': 'No disease detected. Plant appears healthy with vibrant green leaves, no spots or discoloration, normal growth pattern',
        'causes': 'N/A - Plant is healthy',
        'treatment': 'No treatment needed. Continue regular care and monitoring',
        'prevention': 'Maintain current care practices: proper watering, adequate nutrition, good air circulation, regular monitoring for early disease detection',
        'pesticides': 'No pesticides needed. Avoid unnecessary chemical applications',
        'organic_solutions': 'Continue organic practices: compost application, mulching, companion planting, beneficial insects, regular inspection'
    },
    'Potato___Early_blight': {
        'name': 'Potato - Early Blight',
        'symptoms': 'Brown spots with concentric rings on leaves, lower leaves affected first, yellowing between spots, premature defoliation',
        'causes': 'Caused by Alternaria solani fungus, warm temperatures, high humidity, water stress, poor nutrition',
        'treatment': 'Apply fungicide, remove infected leaves, practice crop rotation, mulch around plants',
        'prevention': 'Use certified seed potatoes, maintain plant health, proper spacing, avoid overhead irrigation',
        'pesticides': 'Chlorothalonil, Mancozeb, Copper fungicides',
        'organic_solutions': 'Copper spray, Compost tea, Remove infected foliage'
    },
    'Potato___Late_blight': {
        'name': 'Potato - Late Blight',
        'symptoms': 'Water-soaked spots on leaves, white fungal growth, rapid spreading, tuber rot',
        'causes': 'Phytophthora infestans, cool wet weather, infected seed potatoes',
        'treatment': 'Apply fungicide immediately, remove infected plants, avoid overhead irrigation',
        'prevention': 'Plant resistant varieties, ensure good drainage, monitor weather, destroy infected plants',
        'pesticides': 'Metalaxyl, Chlorothalonil, Mancozeb + Copper',
        'organic_solutions': 'Copper fungicide, Destroy infected plants, Improve drainage'
    },
    'Potato___healthy': {
        'name': 'Healthy Potato Plant',
        'symptoms': 'No disease detected. Plant appears healthy',
        'causes': 'N/A - Plant is healthy',
        'treatment': 'Continue regular care. Monitor for any signs of disease regularly',
        'prevention': 'Maintain proper watering, fertilization, and crop rotation',
        'pesticides': 'No pesticides needed',
        'organic_solutions': 'Continue organic practices and regular monitoring'
    },
    
    # Pepper diseases
    'Pepper___Bacterial_spot': {
        'name': 'Pepper - Bacterial Spot',
        'symptoms': 'Small dark spots on leaves and fruits, yellow halos around spots, leaf drop, fruit lesions reduce marketability',
        'causes': 'Xanthomonas bacteria, warm humid weather, water splash, contaminated seeds, temperatures 75-86°F',
        'treatment': 'Remove infected leaves, apply copper-based bactericides, improve air circulation, avoid overhead watering',
        'prevention': 'Use disease-free seeds, practice crop rotation, maintain plant spacing, remove plant debris, disinfect tools',
        'pesticides': 'Copper hydroxide, Copper sulfate, Streptomycin (early stages), Apply every 7-10 days',
        'organic_solutions': 'Neem oil spray, Copper soap, Bacillus subtilis, Proper sanitation, Resistant varieties'
    },
    'Pepper___healthy': {
        'name': 'Healthy Pepper Plant',
        'symptoms': 'No disease detected. Vibrant green leaves, healthy growth, no spots or discoloration',
        'causes': 'N/A - Plant is healthy',
        'treatment': 'No treatment needed. Continue regular monitoring and care',
        'prevention': 'Maintain good practices: proper watering, nutrition, spacing, and regular inspection',
        'pesticides': 'No pesticides needed',
        'organic_solutions': 'Continue organic practices: mulching, companion planting, beneficial insects'
    },
    
    # Corn diseases
    'Corn___Common_rust': {
        'name': 'Corn - Common Rust',
        'symptoms': 'Small circular to elongate brown pustules on leaves, orange-brown spores, reduced photosynthesis, premature leaf death',
        'causes': 'Puccinia sorghi fungus, moderate temperatures (60-77°F), high humidity, wind-borne spores',
        'treatment': 'Apply fungicides if severe, remove infected leaves, plant resistant hybrids, ensure good air circulation',
        'prevention': 'Use resistant varieties, practice crop rotation, maintain field sanitation, monitor weather conditions',
        'pesticides': 'Azoxystrobin, Propiconazole, Triazole fungicides, Apply at first sign of disease',
        'organic_solutions': 'Sulfur fungicide, Remove infected leaves, Plant resistant varieties, Improve air flow'
    },
    'Corn___Northern_Leaf_Blight': {
        'name': 'Corn - Northern Leaf Blight',
        'symptoms': 'Long cigar-shaped gray-green lesions on leaves, lesions turn tan with age, can cover entire leaf, yield loss',
        'causes': 'Exserohilum turcicum fungus, moderate temperatures (64-81°F), high humidity, infected crop residue',
        'treatment': 'Apply fungicides, remove crop residue, use resistant hybrids, practice crop rotation',
        'prevention': 'Plant resistant hybrids, bury crop residue, rotate crops, maintain field sanitation',
        'pesticides': 'Azoxystrobin, Pyraclostrobin, Propiconazole, Apply preventively in susceptible varieties',
        'organic_solutions': 'Crop rotation, Resistant varieties, Remove residue, Biological fungicides'
    },
    'Corn___healthy': {
        'name': 'Healthy Corn Plant',
        'symptoms': 'No disease detected. Strong green leaves, normal growth, no lesions or discoloration',
        'causes': 'N/A - Plant is healthy',
        'treatment': 'No treatment needed. Continue monitoring throughout growing season',
        'prevention': 'Maintain current practices: adequate nutrition, proper spacing, weed control',
        'pesticides': 'No pesticides needed',
        'organic_solutions': 'Continue good agricultural practices and regular field monitoring'
    },
    
    # Grape diseases
    'Grape___Black_rot': {
        'name': 'Grape - Black Rot',
        'symptoms': 'Circular tan spots on leaves with dark borders, fruit mummies (shriveled black berries), severe yield loss',
        'causes': 'Guignardia bidwellii fungus, warm humid weather (60-90°F), rain splash, infected mummies',
        'treatment': 'Remove mummified berries, apply fungicides, prune for air circulation, sanitation is critical',
        'prevention': 'Remove all mummies, prune properly, apply preventive fungicides, maintain vineyard sanitation',
        'pesticides': 'Mancozeb, Captan, Myclobutanil, Apply from bud break through fruit set',
        'organic_solutions': 'Copper fungicide, Sulfur, Remove mummies, Prune for airflow, Bordeaux mixture'
    },
    'Grape___Leaf_blight': {
        'name': 'Grape - Leaf Blight',
        'symptoms': 'Brown irregular spots on leaves, leaf yellowing, premature defoliation, reduced vine vigor',
        'causes': 'Phomopsis viticola fungus, wet spring weather, infected canes, poor air circulation',
        'treatment': 'Prune infected canes, apply fungicides, improve air circulation, remove fallen leaves',
        'prevention': 'Prune properly, remove infected wood, apply dormant sprays, maintain good canopy management',
        'pesticides': 'Mancozeb, Captan, Ziram, Apply during bud swell and early growth',
        'organic_solutions': 'Lime sulfur (dormant), Copper fungicide, Proper pruning, Canopy management'
    },
    'Grape___healthy': {
        'name': 'Healthy Grape Vine',
        'symptoms': 'No disease detected. Healthy green leaves, normal vine growth, no spots or lesions',
        'causes': 'N/A - Plant is healthy',
        'treatment': 'No treatment needed. Continue regular vineyard management and monitoring',
        'prevention': 'Maintain practices: proper pruning, canopy management, nutrition, pest monitoring',
        'pesticides': 'No pesticides needed',
        'organic_solutions': 'Continue organic viticulture practices and regular inspection'
    }
}
