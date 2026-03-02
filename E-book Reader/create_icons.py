from PIL import Image, ImageDraw
import os
import math

# Create images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

def create_minimal_icon(name, color="#FFFFFF", size=64):
    # Create a new image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Common parameters
    padding = size // 4
    center = size // 2
    icon_size = size - (2 * padding)
    stroke_width = max(2, size // 32)  # Thin, elegant strokes
    
    if name == 'play':
        # Minimal play triangle
        points = [
            (padding + stroke_width, padding),
            (size - padding, center),
            (padding + stroke_width, size - padding)
        ]
        # Draw outline for modern look
        draw.polygon(points, fill=color)
        
    elif name == 'pause':
        # Two minimal lines
        bar_width = size // 8
        spacing = size // 6
        
        # Left bar
        draw.rectangle(
            (center - spacing - bar_width, padding,
             center - spacing, size - padding),
            fill=color
        )
        # Right bar
        draw.rectangle(
            (center + spacing, padding,
             center + spacing + bar_width, size - padding),
            fill=color
        )
        
    elif name == 'stop':
        # Simple square with rounded corners
        radius = size // 16
        draw.rounded_rectangle(
            (padding, padding,
             size - padding, size - padding),
            radius=radius,
            fill=color
        )
        
    elif name == 'open':
        # Minimal folder icon
        height = size - (2 * padding)
        width = height * 1.2
        
        # Main folder body
        points = [
            (padding, padding + height * 0.3),  # Top left
            (padding + width * 0.3, padding + height * 0.3),  # Top middle
            (padding + width * 0.4, padding),  # Tab top
            (size - padding, padding),  # Top right
            (size - padding, size - padding),  # Bottom right
            (padding, size - padding)  # Bottom left
        ]
        draw.polygon(points, fill=color)
        
    elif name == 'settings':
        # Minimal gear icon
        outer_radius = (size - 2 * padding) // 2
        inner_radius = outer_radius * 0.7
        teeth = 8
        
        # Draw gear teeth
        for i in range(teeth):
            angle = i * (360 / teeth)
            rad = math.radians(angle)
            
            # Outer point
            x1 = center + outer_radius * math.cos(rad)
            y1 = center + outer_radius * math.sin(rad)
            
            # Inner point
            x2 = center + inner_radius * math.cos(rad + math.pi/teeth)
            y2 = center + inner_radius * math.sin(rad + math.pi/teeth)
            
            draw.line([(x1, y1), (x2, y2)], fill=color, width=stroke_width)
        
        # Center circle
        draw.ellipse(
            (center - inner_radius//2, center - inner_radius//2,
             center + inner_radius//2, center + inner_radius//2),
            fill=color
        )
    
    elif name == 'bookmark':
        # Minimal bookmark icon
        height = size - padding
        width = size // 3
        points = [
            (center - width//2, padding),  # Top left
            (center + width//2, padding),  # Top right
            (center + width//2, height - padding),  # Bottom right
            (center, height - padding - width//2),  # Bottom middle
            (center - width//2, height - padding),  # Bottom left
        ]
        draw.polygon(points, fill=color)
    
    elif name == 'prev':
        # Modern previous/backward media button (double triangle)
        triangle_width = (size - 2 * padding) // 2
        triangle_height = size - 2 * padding
        
        # First triangle (left)
        points1 = [
            (padding, center),  # Left point
            (padding + triangle_width, padding),  # Top point
            (padding + triangle_width, size - padding),  # Bottom point
        ]
        draw.polygon(points1, fill=color)
        
        # Second triangle (right)
        points2 = [
            (padding + triangle_width, center),  # Left point
            (size - padding, padding),  # Top point
            (size - padding, size - padding),  # Bottom point
        ]
        draw.polygon(points2, fill=color)
        
    elif name == 'next':
        # Modern next/forward media button (double triangle)
        triangle_width = (size - 2 * padding) // 2
        triangle_height = size - 2 * padding
        
        # First triangle (left)
        points1 = [
            (padding, padding),  # Top point
            (padding, size - padding),  # Bottom point
            (padding + triangle_width, center),  # Right point
        ]
        draw.polygon(points1, fill=color)
        
        # Second triangle (right)
        points2 = [
            (padding + triangle_width, padding),  # Top point
            (padding + triangle_width, size - padding),  # Bottom point
            (size - padding, center),  # Right point
        ]
        draw.polygon(points2, fill=color)
    
    elif name == 'highlight':
        # Minimal highlight marker
        height = size - (2 * padding)
        width = height * 0.8
        points = [
            (padding, padding + height * 0.2),  # Top left
            (padding + width, padding),  # Top right
            (padding + width, padding + height * 0.6),  # Bottom right
            (padding, padding + height * 0.8),  # Bottom left
        ]
        draw.polygon(points, fill=color)
    
    # Save with high quality
    img.save(f'images/{name}.png', 'PNG', quality=95)

# Create all icons
icons = ['play', 'pause', 'stop', 'open', 'settings', 'bookmark', 'highlight', 'prev', 'next']
for icon in icons:
    # Create multiple sizes for different uses
    create_minimal_icon(icon, size=64)  # Regular size
    create_minimal_icon(icon, size=32)  # Small size
    create_minimal_icon(icon, size=24)  # Toolbar size 