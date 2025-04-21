import csv
from datetime import datetime
import os

def prompt_input(prompt_text, required=True):
    while True:
        value = input(f"{prompt_text}: ").strip()
        if value or not required:
            return value

def get_ingredients():
    ingredients = []
    print("\nEnter ingredients (leave name blank to finish):")
    while True:
        name = input("  Ingredient name: ").strip()
        if not name:
            break
        quantity = input("  Quantity: ").strip()
        ingredients.append((name, quantity))
    return ingredients

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        print("❌ Date format should be YYYY-MM-DD. Try again.")
        return None

def get_valid_date():
    while True:
        date_str = input("Date posted (YYYY-MM-DD, optional): ").strip()
        if not date_str:
            return "Unknown"
        valid = validate_date(date_str)
        if valid:
            return valid

def get_next_recipe_id(csv_path):
    if not os.path.exists(csv_path):
        return 100001  # start fresh
    with open(csv_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        ids = [int(row['id']) for row in reader if row['id'].isdigit()]
        return max(ids) + 1 if ids else 100001

def append_to_csv(recipe, ingredients, recipe_csv="recipes.csv", ingredients_csv="ingredients.csv"):
    recipe_exists = os.path.exists(recipe_csv)
    ingredients_exist = os.path.exists(ingredients_csv)

    with open(recipe_csv, "a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not recipe_exists:
            writer.writerow(["id", "name", "instructions", "source", "source_author", "date_posted", "license", "description", "image_url", "tags"])
        writer.writerow(recipe)

    with open(ingredients_csv, "a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not ingredients_exist:
            writer.writerow(["recipe_id", "ingredient_name", "quantity"])
        for name, qty in ingredients:
            writer.writerow([recipe[0], name, qty])

def main():
    print("Add a New Recipe\n" + "-"*25)

    recipe_id = get_next_recipe_id("recipes.csv")
    name = prompt_input("Recipe name")
    instructions = prompt_input("Instructions")
    source = prompt_input("Source URL", required=False)
    author = prompt_input("Author", required=False) or "Unknown"
    date_posted = get_valid_date()
    license_info = prompt_input("License (e.g., CC-BY-SA)", required=False) or "Unknown"
    description = prompt_input("Short description", required=False) or "Unknown"
    image_url = prompt_input("Image URL", required=False) or "Unknown"
    tags = prompt_input("Tags (comma separated)", required=False)
    tag_str = "|".join(tag.strip() for tag in tags.split(",") if tag.strip()) if tags else ""

    ingredients = get_ingredients()

    recipe_row = [
        recipe_id, name, instructions, source, author,
        date_posted, license_info, description, image_url, tag_str
    ]

    append_to_csv(recipe_row, ingredients)
    print(f"\nRecipe '{name}' added successfully with ID {recipe_id}!")

if __name__ == "__main__":
    main()
