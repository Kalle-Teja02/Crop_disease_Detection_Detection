#!/usr/bin/env python3
"""
Generate synthetic Corn Common Rust images for training
Creates realistic disease images using image processing
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import random

# Create dataset directory
dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'Corn___Common_rust')
os.makedirs(dataset_path, exist_ok=True)

print("="*70)
print("GENERATING SYNTHETIC CORN COMMON RUST IMAGES")
print("="*70)
print(f"Output directory: {dataset_path}\n")

def create_leaf_base(width=256, height=256):
    """Create a base corn leaf image"""
    img = Image.new('RGB', (width, height), (34, 139, 34))  # Dark green
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Draw leaf shape (elongated)
    points = [
        (width//2, 20),
        (width//2 + 40, 60),
        (width//2 + 50, height//2),
        (width//2 + 40, height - 60),
        (width//2, height - 20),
        (width//2 - 40, height - 60),
        (width//2 - 50, height//2),
        (width//2 - 40, 60),
    ]
    draw.polygon(points, fill=(34, 139, 34, 255))
    
    # Add leaf veins
    for i in range(5):
        x = width//2 - 30 + i*15
        draw.line([(x, 20), (x, height-20)], fill=(20, 100, 20, 200), width=2)
    
    return img

def add_rust_spots(img, num_spots=15):
    """Add rust-colored spots to simulate common rust disease"""
    img = img.copy()
    draw = ImageDraw.Draw(img, 'RGBA')
    width, height = img.size
    
    rust_colors = [
        (139, 69, 19, 180),    # Brown
        (165, 42, 42, 180),    # Dark red
        (178, 34, 34, 180),    # Firebrick
        (205, 92, 92, 180),    # Indian red
        (160, 82, 45, 180),    # Sienna
    ]
    
    for _ in range(num_spots):
        # Random position
        x = random.randint(width//4, 3*width//4)
        y = random.randint(height//4, 3*height//4)
        
        # Random size
        radius = random.randint(8, 25)
        
        # Random rust color
        color = random.choice(rust_colors)
        
        # Draw rust spot (circle with irregular edges)
        for i in range(radius, 0, -2):
            alpha = int(color[3] * (1 - i/radius))
            draw.ellipse(
                [(x-i, y-i), (x+i, y+i)],
                fill=(*color[:3], alpha)
            )
    
    return img

def add_texture(img):
    """Add texture to make image more realistic"""
    img = img.copy()
    
    # Add slight blur
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    # Add noise
    img_array = np.array(img, dtype=np.float32)
    noise = np.random.normal(0, 5, img_array.shape)
    img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(img_array)
    
    # Adjust contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    
    return img

def create_rust_image(image_num):
    """Create a single rust image with variations"""
    # Create base leaf
    img = create_leaf_base(256, 256)
    
    # Add rust spots
    num_spots = random.randint(10, 25)
    img = add_rust_spots(img, num_spots)
    
    # Add texture
    img = add_texture(img)
    
    # Random rotation
    angle = random.randint(-15, 15)
    img = img.rotate(angle, expand=False)
    
    # Random brightness
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(random.uniform(0.8, 1.2))
    
    return img

# Generate images
print("Generating 50 synthetic corn common rust images...\n")

for i in range(50):
    img = create_rust_image(i)
    filename = os.path.join(dataset_path, f'synthetic_rust_{i:03d}.jpg')
    img.save(filename, 'JPEG', quality=90)
    
    if (i + 1) % 10 == 0:
        print(f"✅ Generated {i + 1}/50 images")

print(f"\n✅ Successfully generated 50 synthetic images!")
print(f"📁 Location: {dataset_path}")
print(f"\nNow run: python train_cnn_model.py")
print("="*70)
