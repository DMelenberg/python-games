"""
Generate artistic, hand-painted style textures for 2048 game.
Inspired by organic, flowing designs with rich colors and textures.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import random
import math
import os

def add_noise(img, intensity=15):
    """Add subtle noise for organic texture."""
    pixels = img.load()
    width, height = img.size
    for x in range(width):
        for y in range(height):
            if random.random() < 0.3:  # 30% of pixels
                r, g, b = pixels[x, y][:3] if len(pixels[x, y]) >= 3 else (pixels[x, y], pixels[x, y], pixels[x, y])
                noise = random.randint(-intensity, intensity)
                r = max(0, min(255, r + noise))
                g = max(0, min(255, g + noise))
                b = max(0, min(255, b + noise))
                if img.mode == 'RGBA':
                    pixels[x, y] = (r, g, b, pixels[x, y][3])
                else:
                    pixels[x, y] = (r, g, b)
    return img

def create_organic_gradient(width, height, colors, flow_strength=0.3):
    """Create flowing, organic gradient with multiple colors."""
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    
    # Create flowing pattern using sine waves
    for y in range(height):
        for x in range(width):
            # Multiple sine wave layers for organic feel
            wave1 = math.sin(x * 0.02 + y * 0.01) * 0.5 + 0.5
            wave2 = math.sin(x * 0.03 - y * 0.02) * 0.5 + 0.5
            wave3 = math.sin((x + y) * 0.015) * 0.5 + 0.5
            
            # Combine waves
            t = (wave1 * 0.4 + wave2 * 0.3 + wave3 * 0.3)
            
            # Add position-based gradient
            position = (y / height) * 0.6 + t * 0.4
            
            # Interpolate through color stops
            if len(colors) == 2:
                color = interpolate_color(colors[0], colors[1], position)
            else:
                # Multiple color stops
                segment = position * (len(colors) - 1)
                idx = int(segment)
                if idx >= len(colors) - 1:
                    color = colors[-1]
                else:
                    local_t = segment - idx
                    color = interpolate_color(colors[idx], colors[idx + 1], local_t)
            
            pixels[x, y] = color
    
    return img

def interpolate_color(color1, color2, t):
    """Interpolate between two colors."""
    r = int(color1[0] + (color2[0] - color1[0]) * t)
    g = int(color1[1] + (color2[1] - color1[1]) * t)
    b = int(color1[2] + (color2[2] - color1[2]) * t)
    return (r, g, b)

def add_organic_overlay(img, intensity=30):
    """Add organic, painterly overlay."""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    width, height = img.size
    
    # Add subtle organic shapes
    for _ in range(20):
        x = random.randint(-width//4, width)
        y = random.randint(-height//4, height)
        size = random.randint(width//6, width//3)
        alpha = random.randint(10, intensity)
        
        # Random light or dark
        if random.random() > 0.5:
            color = (255, 255, 255, alpha)
        else:
            color = (0, 0, 0, alpha//2)
        
        draw.ellipse([x, y, x + size, y + size], fill=color)
    
    # Blur for organic feel
    overlay = overlay.filter(ImageFilter.GaussianBlur(40))
    
    img_rgba = img.convert('RGBA')
    return Image.alpha_composite(img_rgba, overlay)

def add_border_glow(img, color, width=8):
    """Add glowing border around tile."""
    glow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    
    w, h = img.size
    
    # Multiple layers for glow effect
    for i in range(width, 0, -1):
        alpha = int(80 * (width - i) / width)
        draw.rounded_rectangle(
            [(i, i), (w - i, h - i)],
            radius=15,
            outline=(*color, alpha),
            width=2
        )
    
    glow = glow.filter(ImageFilter.GaussianBlur(5))
    
    img_rgba = img.convert('RGBA')
    return Image.alpha_composite(img_rgba, glow)

def create_artistic_tile(size, color_palette, value, border_color=None):
    """Create artistic, hand-painted style tile."""
    # Create organic gradient base
    tile = create_organic_gradient(size, size, color_palette, flow_strength=0.3)
    
    # Add noise for texture
    tile = add_noise(tile, intensity=12)
    
    # Add organic overlay
    tile = add_organic_overlay(tile, intensity=25)
    
    # Slightly blur for painted effect
    tile = tile.filter(ImageFilter.GaussianBlur(0.5))
    
    # Add border glow if specified
    if border_color and value > 0:
        tile = add_border_glow(tile, border_color, width=6)
    
    # Create rounded corners mask
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (size, size)], radius=20, fill=255)
    
    tile_rgba = tile.convert('RGBA')
    tile_rgba.putalpha(mask)
    
    return tile_rgba

def create_flowing_background(width, height):
    """Create flowing, layered background like the examples."""
    # Multiple color layers creating depth
    layers = [
        [(180, 200, 190), (160, 185, 175), (140, 170, 165)],  # Base aqua
        [(220, 210, 180), (200, 185, 150), (180, 165, 130)],  # Sandy yellow
        [(210, 180, 140), (190, 160, 120), (170, 140, 100)],  # Warm orange
        [(160, 195, 180), (140, 175, 165), (120, 155, 150)],  # Teal accent
    ]
    
    bg = Image.new('RGBA', (width, height), (185, 200, 195, 255))
    
    # Create flowing wave layers
    for layer_idx, colors in enumerate(layers):
        layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        
        # Create wave shapes
        points = []
        wave_height = height // len(layers)
        y_offset = height - (layer_idx + 1) * wave_height
        
        for x in range(0, width + 50, 10):
            # Multiple sine waves for organic flow
            y = y_offset + \
                math.sin(x * 0.01 + layer_idx) * 30 + \
                math.sin(x * 0.03 + layer_idx * 0.5) * 15
            points.append((x, y))
        
        # Complete the polygon
        points.append((width, height))
        points.append((0, height))
        
        # Fill with gradient-ish color
        draw.polygon(points, fill=(*colors[0], 200))
        
        # Add noise
        layer = add_noise(layer, intensity=8)
        
        # Blur edges
        layer = layer.filter(ImageFilter.GaussianBlur(3))
        
        bg = Image.alpha_composite(bg, layer)
    
    return bg

def main():
    textures_dir = os.path.join(os.path.dirname(__file__), 'textures')
    os.makedirs(textures_dir, exist_ok=True)
    
    print("Generating artistic hand-painted textures...")
    
    tile_size = 256
    
    # Artistic color palettes inspired by the examples
    # Each tile has unique organic colors
    tile_palettes = {
        0: {
            'colors': [(235, 230, 220), (220, 215, 205), (210, 205, 195)],
            'border': (200, 195, 185)
        },
        2: {
            'colors': [(255, 250, 235), (245, 235, 215), (235, 220, 200)],
            'border': (220, 200, 170)
        },
        4: {
            'colors': [(255, 240, 210), (245, 225, 190), (235, 210, 170)],
            'border': (210, 180, 140)
        },
        8: {
            'colors': [(255, 215, 160), (245, 195, 135), (235, 175, 115)],
            'border': (210, 150, 90)
        },
        16: {
            'colors': [(255, 190, 130), (245, 165, 100), (235, 145, 80)],
            'border': (200, 120, 60)
        },
        32: {
            'colors': [(255, 160, 110), (245, 135, 85), (235, 115, 65)],
            'border': (200, 90, 45)
        },
        64: {
            'colors': [(255, 130, 90), (245, 105, 65), (235, 85, 50)],
            'border': (200, 65, 30)
        },
        128: {
            'colors': [(255, 235, 150), (245, 215, 120), (235, 195, 100)],
            'border': (210, 170, 80)
        },
        256: {
            'colors': [(255, 225, 130), (245, 205, 100), (235, 185, 80)],
            'border': (210, 160, 60)
        },
        512: {
            'colors': [(255, 215, 110), (245, 195, 85), (235, 175, 65)],
            'border': (210, 150, 45)
        },
        1024: {
            'colors': [(255, 205, 90), (245, 185, 70), (235, 165, 55)],
            'border': (210, 140, 35)
        },
        2048: {
            'colors': [(255, 195, 70), (245, 175, 55), (235, 155, 40)],
            'border': (210, 130, 25)
        },
    }
    
    for value, palette in tile_palettes.items():
        tile = create_artistic_tile(
            tile_size, 
            palette['colors'],
            value,
            palette['border']
        )
        filename = f'{textures_dir}/tile_{value}.png'
        tile.save(filename, 'PNG')
        print(f"✓ tile_{value}.png")
    
    # Create flowing background
    bg = create_flowing_background(600, 600)
    bg.save(f'{textures_dir}/background.png', 'PNG')
    print("✓ background.png")
    
    print("\nAll artistic textures generated successfully!")
    print("Style: Organic, hand-painted with flowing gradients")

if __name__ == "__main__":
    main()
