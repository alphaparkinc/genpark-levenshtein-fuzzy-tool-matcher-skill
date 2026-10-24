"""Example usage for GenPark Levenshtein Fuzzy Tool Matcher."""
from client import LevenshteinFuzzyToolMatcher

def main():
    tools = [
        "web_search_crawler",
        "sql_database_query",
        "fetch_weather_forecast",
        "read_json_document"
    ]

    typo_call = "fetch_wether_forcast"
    print(f"Repairing hallucinated tool call: '{typo_call}'")
    match = LevenshteinFuzzyToolMatcher.find_best_match(typo_call, tools)
    print(f"Autocorrected to: '{match['matched_candidate']}' (Similarity: {match['similarity']})")

    print("
Ranked suggestions for 'search_web':")
    suggestions = LevenshteinFuzzyToolMatcher.suggest_alternatives("search_web", tools, top_k=2)
    for s in suggestions:
        print(f" - {s['candidate']}: similarity={s['similarity']}")

if __name__ == "__main__":
    main()
