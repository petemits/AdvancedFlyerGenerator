from PIL import Image, ImageDraw, ImageFont
import math
import random
import os
from datetime import datetime

class SmartFlyerGenerator:
    def __init__(self):
        self.output_folder = "smart_flyers"
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
    
    def generate_math_pattern(self, draw, width, height):
        """Generate mathematical background patterns - FIXED VERSION"""
        # Safer pattern generation
        for i in range(80):  # Reduced number for safety
            x = random.randint(50, width - 50)
            y = random.randint(50, height - 50)
            
            # Ensure size is positive and reasonable
            size = abs(int(5 + 15 * math.sin(x/50) * math.cos(y/50)))
            size = max(5, min(size, 30))  # Limit size between 5 and 30
            
            # Calculate coordinates safely
            x0 = max(0, x - size//2)
            y0 = max(0, y - size//2)
            x1 = min(width, x + size//2)
            y1 = min(height, y + size//2)
            
            # Ensure valid coordinates
            if x0 < x1 and y0 < y1:
                color = (
                    int(128 + 127 * math.sin(x/100)),
                    int(128 + 127 * math.cos(y/100)),
                    int(128 + 127 * math.sin((x+y)/100))
                )
                draw.ellipse([x0, y0, x1, y1], fill=color, outline=None)
    
    def calculate_golden_ratio_layout(self, width, height):
        """Use golden ratio for aesthetically pleasing layouts"""
        phi = (1 + math.sqrt(5)) / 2  # Golden ratio
        
        return {
            'title_area': (0, 0, width, int(height/phi)),
            'content_area': (0, int(height/phi), width, height),
            'image_area': (int(width/phi), 0, width, int(height/phi))
        }
    
    def create_smart_flyer(self, title, description, details):
        width, height = 800, 1200
        
        # Create base image with gradient
        image = Image.new('RGB', (width, height), color=(30, 30, 60))
        draw = ImageDraw.Draw(image)
        
        # Add mathematical background pattern
        self.generate_math_pattern(draw, width, height)
        
        # Calculate layout using golden ratio
        layout = self.calculate_golden_ratio_layout(width, height)
        
        # Add text with mathematical positioning
        try:
            title_font = ImageFont.truetype("arial.ttf", 48)
            desc_font = ImageFont.truetype("arial.ttf", 24)
        except:
            # Use default font if arial is not available
            title_font = ImageFont.load_default()
            desc_font = ImageFont.load_default()
        
        # Position title using golden ratio
        title_x = width // 10
        title_y = layout['title_area'][3] // 3
        draw.text((title_x, title_y), title, fill=(255, 255, 255), font=title_font)
        
        # Add description with word wrap
        words = description.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=desc_font)
            test_width = bbox[2] - bbox[0]
            
            if test_width < width - 100:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw description lines
        desc_y = layout['content_area'][1] + 50
        for line in lines:
            draw.text((50, desc_y), line, fill=(255, 255, 255), font=desc_font)
            desc_y += 40
        
        # Add details with mathematical spacing
        detail_y = desc_y + 30
        for detail in details:
            draw.text((50, detail_y), f"• {detail}", fill=(200, 200, 255), font=desc_font)
            detail_y += 35
        
        # Add mathematical decoration
        self.add_mathematical_decoration(draw, width, height)
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_folder}/smart_flyer_{timestamp}.png"
        image.save(filename)
        
        return filename
    
    def add_mathematical_decoration(self, draw, width, height):
        """Add mathematical elements as decoration - FIXED VERSION"""
        # Draw coordinate system
        draw.line([50, height-50, width-50, height-50], fill=(255, 255, 255, 100), width=2)
        draw.line([50, 50, 50, height-50], fill=(255, 255, 255, 100), width=2)
        
        # Draw function graphs safely
        for x in range(50, width-50, 5):
            # Sine wave with bounds checking
            y1 = int(height/2 + math.sin((x-50)/30) * 100)
            y1 = max(50, min(y1, height-50))  # Keep within bounds
            
            # Cosine wave with bounds checking
            y2 = int(height/2 + math.cos((x-50)/25) * 80)
            y2 = max(50, min(y2, height-50))  # Keep within bounds
            
            # Draw points only if they're within bounds
            if 50 <= y1 <= height-50:
                draw.ellipse([x, y1, x+2, y1+2], fill=(255, 100, 100))
            
            if 50 <= y2 <= height-50:
                draw.ellipse([x, y2, x+2, y2+2], fill=(100, 255, 100))

class FlyerAnnouncer:
    def __init__(self):
        self.tts_available = False
        # Comment out TTS for now to avoid any issues
        print("Text-to-speech disabled for stability")
    
    def announce_flyer(self, title, description):
        # Simple print instead of TTS
        print(f"📢 Flyer Announcement: {title} - {description}")

def main():
    # Initialize components
    flyer_generator = SmartFlyerGenerator()
    announcer = FlyerAnnouncer()
    
    # Sample content with mathematical/AI themes
    flyers = [
        {
            "title": "Data Science Workshop",
            "description": "Learn advanced mathematical concepts and AI algorithms",
            "details": ["Linear Algebra", "Probability & Statistics", "Machine Learning", "Hands-on Projects"]
        },
        {
            "title": "Math Art Exhibition",
            "description": "Exploring mathematical patterns in digital art",
            "details": ["Fractal Art", "Algorithmic Design", "Interactive Installations"]
        }
    ]
    
    print("Generating smart flyers with mathematical elements...")
    
    for i, flyer in enumerate(flyers, 1):
        print(f"Creating flyer {i} of {len(flyers)}...")
        
        try:
            # Generate the flyer
            filename = flyer_generator.create_smart_flyer(
                flyer["title"],
                flyer["description"],
                flyer["details"]
            )
            
            # Announce the flyer creation
            announcer.announce_flyer(flyer["title"], flyer["description"])
            
            print(f"✓ Created: {filename}")
            
        except Exception as e:
            print(f"✗ Error creating flyer {i}: {e}")
            continue
    
    print(f"\n🎉 Flyer generation completed!")
    print(f"📁 Location: {os.path.abspath(flyer_generator.output_folder)}")

if __name__ == "__main__":
    main()