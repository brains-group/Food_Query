import requests


def fetch_meals(search_query=""):
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={search_query}"
    response = requests.get(url)
    data = response.json()

    meals = data.get("meals")
    if not meals:
        print("No meals found.")
        return []

    recipes = []
    for meal in meals:
        recipe = {
            "recipe_name": meal.get("strMeal"),
            "author": meal.get("strSource") or "Unknown",
            "ingredients": [],
            "steps": meal.get("strInstructions")
        }

        for i in range(1, 21):
            ingredient = meal.get(f"strIngredient{i}")
            measure = meal.get(f"strMeasure{i}")
            if ingredient and ingredient.strip():
                recipe["ingredients"].append(f"{measure.strip()} {ingredient.strip()}")

        recipes.append(recipe)

    return recipes


# Example usage
if __name__ == "__main__":
    search_term = input("Search for meals: ")
    results = fetch_meals(search_term)

    for idx, r in enumerate(results):
        print(f"\n=== RECIPE {idx + 1}: {r['recipe_name']} ===")
        print(f"Author/Source: {r['author']}")
        print("\nIngredients:")
        for ing in r['ingredients']:
            print(f"- {ing}")
        print("\nInstructions:")
        print(r['steps'])
