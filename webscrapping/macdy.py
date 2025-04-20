from pdf2image import convert_from_path

images = convert_from_path("DownloadNutritionInfo.pdf", dpi=300)
for i, img in enumerate(images):
    img.save(f"page_{i}.png", "PNG")

from PIL import Image
import pytesseract

# Example for the first page
text = pytesseract.image_to_string(Image.open("page_0.png"))
print(text[:1000])  # Preview the extracted text

import pandas as pd

# Let's say you split the lines by newlines and tabs
lines = text.split('\n')
data = []

for line in lines:
    # Example: splitting based on 2+ spaces or tabs
    parts = [p.strip() for p in line.split("  ") if p.strip()]
    if len(parts) >= 3:  # adjust based on expected fields
        data.append(parts)

# Convert to CSV
df = pd.DataFrame(data)
df.to_csv("output.csv", index=False)

# Or to JSON
df.to_json("output.json", orient="records", indent=2)
