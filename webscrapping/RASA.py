import requests
from bs4 import BeautifulSoup
import json

def get_locations():
    url = "https://www.rasa.co/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        location_section = soup.find("section", id="our-locations-stripe")
        locations = []

        if location_section:
            raw_text = location_section.get_text(separator="\n", strip=True)
            lines = raw_text.split("\n")

            current_state = None
            for line in lines:
                if line.lower() in ["dc", "maryland", "virginia"]:
                    current_state = line
                elif any(char.isdigit() for char in line):  # Address line
                    if current_state:
                        locations.append({
                            "state": current_state,
                            "address": line
                        })
        return locations

    except Exception as e:
        print("Error fetching locations:", e)
        return []

def get_menu():
    url = "https://www.rasa.co/menu#menu-opening"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        menu_items = []

        main_tag = soup.find("main", class_="Index")
        if not main_tag:
            print("Main menu section not found.")
            return []

        sections = main_tag.find_all("section", class_="Index-page")
        for section in sections:
            heading = section.find("h2")
            category = heading.get_text(strip=True) if heading else "Uncategorized"
            cards = section.find_all("figcaption", class_="image-card-wrapper")
            blocks = section.find_all("div", class_="col sqs-col-4 span-4")

            for i, card in enumerate(cards):
                name_tag = card.find("div", class_="image-title-wrapper")
                desc_tag = card.find("div", class_="image-subtitle sqs-dynamic-text")
                name = name_tag.get_text(strip=True) if name_tag else None
                item = {
                    "category": category,
                    "name": name
                }

                if desc_tag:
                    # Extract <strong> tags as special features
                    strong_tags = desc_tag.find_all("strong")
                    if strong_tags:
                        item["tag"] = [tag.get_text(strip=True) for tag in strong_tags if tag.get_text(strip=True)]

                    # Handle multiple paragraphs as options
                    p_tags = desc_tag.find_all("p")
                    if len(p_tags) > 1:
                        item["options"] = [p.get_text(strip=True) for p in p_tags if p.get_text(strip=True)]
                    else:
                        description = desc_tag.get_text(strip=True)
                        if description:
                            item["description"] = description

                # Try extracting options from the matching block if available
                if i < len(blocks):
                    block = blocks[i]
                    html_content = block.find("div", class_="sqs-html-content")
                    if html_content:
                        block_p_tags = html_content.find_all("p")
                        if block_p_tags:
                            # Extract <strong> tags from each <p>
                            # block_strong_tags = []
                            # for p in block_p_tags:
                            #     block_strong_tags.extend(p.find_all("strong"))

                            # if block_strong_tags:
                            #     item["tag"] = [tag.get_text(strip=True) for tag in block_strong_tags if tag.get_text(strip=True)]

                            item["options"] = [p.get_text(strip=True) for p in block_p_tags if p.get_text(strip=True)]
                if category:
                    menu_items.append(item)

        return menu_items

    except Exception as e:
        print("Error fetching menu:", e)
        return []




def main():
    data = {
        "restaurant": "Rasa",
        "locations": get_locations(),
        "menu": get_menu(),
        "contact_info": "https://www.rasa.co/"  # could be extended
    }

    # Save to file
    with open("rasa_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("Scraped data saved to rasa_data.json")

if __name__ == "__main__":
    main()
