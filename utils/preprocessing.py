"""
Image Preprocessing Module
Handles image loading, resizing, and normalization for CNN
"""

import numpy as np
from PIL import Image
import os


class ImagePreprocessor:
    """Preprocesses images for CNN model prediction"""
    
    def __init__(self, target_size=(128, 128)):
        """
        Initialize preprocessor
        
        Args:
            target_size: Tuple of (height, width) for resizing
        """
        self.target_size = target_size
    
    def load_image(self, image_path):
        """
        Load image from file path
        
        Args:
            image_path: Path to image file
            
        Returns:
            PIL Image object or None if error
        """
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found: {image_path}")
            
            img = Image.open(image_path).convert('RGB')
            return img
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    def resize_image(self, img, size=None):
        """
        Resize image to target size
        
        Args:
            img: PIL Image object
            size: Optional custom size, defaults to self.target_size
            
        Returns:
            Resized PIL Image
        """
        if size is None:
            size = self.target_size
        
        return img.resize(size, Image.Resampling.LANCZOS)
    
    def normalize_image(self, img_array):
        """
        Normalize image array to 0-1 range
        
        Args:
            img_array: Numpy array of image
            
        Returns:
            Normalized numpy array (float32)
        """
        return np.array(img_array, dtype=np.float32) / 255.0
    
    def preprocess(self, image_path):
        """
        Complete preprocessing pipeline for CNN
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dict with:
                - 'success': bool
                - 'data': preprocessed numpy array (1, 3, height, width) for PyTorch
                - 'error': error message if failed
        """
        try:
            # Load image
            img = self.load_image(image_path)
            if img is None:
                return {
                    'success': False,
                    'data': None,
                    'error': 'Failed to load image'
                }
            
            # Resize
            img = self.resize_image(img)
            
            # Convert to array
            img_array = np.array(img)
            
            # Normalize
            img_array = self.normalize_image(img_array)
            
            # Transpose to channels-first format for PyTorch (batch, channels, height, width)
            img_array = np.transpose(img_array, (2, 0, 1))
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return {
                'success': True,
                'data': img_array,
                'error': None
            }
        
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': str(e)
            }
