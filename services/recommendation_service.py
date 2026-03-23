"""
Recommendation Service Layer
Handles disease recommendations and confidence-based warnings
"""

from disease_info import disease_data


class RecommendationService:
    """Service for generating disease recommendations"""
    
    CONFIDENCE_THRESHOLD = 0.60  # 60% confidence threshold
    
    def __init__(self, confidence_threshold=None):
        """
        Initialize recommendation service
        
        Args:
            confidence_threshold: Confidence threshold (0-1). Default 0.60
        """
        if confidence_threshold is not None:
            self.CONFIDENCE_THRESHOLD = confidence_threshold
    
    def get_recommendation(self, predicted_class, confidence):
        """
        Get disease recommendation with confidence handling
        
        Args:
            predicted_class: Predicted disease class name
            confidence: Confidence score (0-100)
            
        Returns:
            Dict with:
                - 'disease': disease name
                - 'confidence': confidence score
                - 'treatment': treatment information
                - 'symptoms': symptoms information
                - 'causes': causes information
                - 'prevention': prevention information
                - 'pesticides': pesticide information
                - 'organic_solutions': organic solutions
                - 'warning': warning message if low confidence
                - 'is_low_confidence': bool
        """
        try:
            # Normalize confidence to 0-1 range if needed
            conf_normalized = confidence / 100.0 if confidence > 1 else confidence
            is_low_confidence = conf_normalized < self.CONFIDENCE_THRESHOLD
            
            # Get disease info
            disease_info = disease_data.get(predicted_class, None)
            
            if disease_info is None:
                # Fallback if disease not found
                disease_name = predicted_class.replace('___', ' - ').replace('_', ' ')
                disease_info = {
                    'name': disease_name,
                    'symptoms': 'Information not available',
                    'treatment': 'Consult agricultural expert',
                    'causes': 'Information not available',
                    'prevention': 'Information not available',
                    'pesticides': 'Information not available',
                    'organic_solutions': 'Information not available'
                }
            
            # Build recommendation
            recommendation = {
                'disease': disease_info.get('name', predicted_class),
                'confidence': confidence,
                'treatment': disease_info.get('treatment', 'Consult agricultural expert'),
                'symptoms': disease_info.get('symptoms', 'Information not available'),
                'causes': disease_info.get('causes', 'Information not available'),
                'prevention': disease_info.get('prevention', 'Information not available'),
                'pesticides': disease_info.get('pesticides', 'Information not available'),
                'organic_solutions': disease_info.get('organic_solutions', 'Information not available'),
                'is_low_confidence': is_low_confidence,
                'warning': None
            }
            
            # Add warning if low confidence
            if is_low_confidence:
                recommendation['warning'] = (
                    f"Low confidence ({confidence:.1f}%). "
                    f"This prediction may not be accurate. "
                    f"Please verify with an agricultural expert."
                )
            
            return recommendation
        
        except Exception as e:
            return {
                'disease': 'Unknown',
                'confidence': 0,
                'treatment': 'Error occurred',
                'symptoms': str(e),
                'causes': 'Error',
                'prevention': 'Error',
                'pesticides': 'Error',
                'organic_solutions': 'Error',
                'is_low_confidence': True,
                'warning': f'Error generating recommendation: {str(e)}'
            }
    
    def set_confidence_threshold(self, threshold):
        """
        Set confidence threshold
        
        Args:
            threshold: Threshold value (0-1)
        """
        if 0 <= threshold <= 1:
            self.CONFIDENCE_THRESHOLD = threshold
        else:
            raise ValueError("Threshold must be between 0 and 1")
