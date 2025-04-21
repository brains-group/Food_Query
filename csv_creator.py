import requests
from bs4 import BeautifulSoup
import csv


def fetch_meals(search_query=""):
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={search_query}"
    response = requests.get(url)
    data = response.json()
    return data.get("meals", [])


def get_author_from_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.content, 'html.parser')

        meta_author = soup.find("meta", {"name": "author"})
        if meta_author and meta_author.get("content"):
            return meta_author["content"].strip()

        og_author = soup.find("meta", {"property": "og:author"})
        if og_author and og_author.get("content"):
            return og_author["content"].strip()

        if "youtube.com" in url:
            title = soup.title.string if soup.title else ""
            if " - YouTube" in title:
                return title.replace(" - YouTube", "").strip()

        potential_links = soup.find_all("a", href=True)
        for link in potential_links:
            href = link["href"].lower()
            classnames = " ".join(link.get("class", [])).lower()
            text = link.get_text(strip=True)

            if (
                any(k in href for k in ["/author", "/user", "/profile", "/contributor"]) or
                any(k in classnames for k in ["author", "byline", "contributor", "writer"])
            ) and text:
                return text

    except Exception as e:
        print(f"Could not get author from {url}: {e}")

    return "Unknown"


def save_to_csv(meals):
    # Recipes file
    with open("recipes.csv", "w", newline='', encoding='utf-8') as recipe_file:
        recipe_writer = csv.writer(recipe_file)
        recipe_writer.writerow(["id", "name", "instructions", "source", "source_author"])

        for meal in meals:
            meal_id = meal.get("idMeal")
            name = meal.get("strMeal")
            instructions = meal.get("strInstructions", "").replace("\n", " ").strip()
            source = meal.get("strSource") or ""
            source_author = get_author_from_url(source) if source else "Unknown"
            recipe_writer.writerow([meal_id, name, instructions, source, source_author])

    # Ingredients file
    with open("ingredients.csv", "w", newline='', encoding='utf-8') as ingredients_file:
        ingredients_writer = csv.writer(ingredients_file)
        ingredients_writer.writerow(["recipe_id", "ingredient_name", "quantity"])

        for meal in meals:
            meal_id = meal.get("idMeal")
            for i in range(1, 21):
                ingredient = meal.get(f"strIngredient{i}")
                quantity = meal.get(f"strMeasure{i}")
                if ingredient and ingredient.strip():
                    ingredients_writer.writerow([meal_id, ingredient.strip(), quantity.strip()])


if __name__ == "__main__":
    all_meals = fetch_meals("")  # Fetch meals
    if all_meals:
        save_to_csv(all_meals)
        print("Data saved to 'recipes.csv' and 'ingredients.csv' with source authors!")
    else:
        print("No meals found.")