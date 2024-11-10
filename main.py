import requests

def ask_questions():
    questions = [
        "Who are you buying the gift for? (e.g., friend, parent, spouse, etc.)",
        "What is the recipient's age group? (e.g., child, teenager, adult, senior)",
        "What are some of their interests? (e.g., books, sports, tech, art)",
        "What’s the occasion? (e.g., birthday, anniversary, holiday)",
        "Do they have any favorite hobbies? (e.g., gardening, cooking, painting)",
        "What is your budget range? (e.g., $20-50, $50-100, etc.)",
        "Are you looking for something personalized?",
        "Do you want the gift to be practical, sentimental, or fun?",
        "What size or type of gift are you considering? (e.g., small, medium, large)",
        "Do you have any color preferences for the gift?",
    ]
    
    responses = {}
    for question in questions:
        responses[question] = input(question + "\n")
    
    return responses

def generate_search_query(responses):
    # Generate a search query based on the responses for specific keywords
    query = f"{responses['Who are you buying the gift for?']} gift for {responses['What’s the occasion?']} {responses['What are some of their interests?']}"
    return query

def search_product(query):
    # Placeholder function to demonstrate search API call
    url = "https://api.example.com/search"  # Replace with actual e-commerce API endpoint
    params = {
        "q": query,
        "sort": "relevance",
        "api_key": "YOUR_API_KEY"  # Replace with your actual API key
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        products = response.json()["items"]
        return products[:3]  # Return the top 3 product matches
    else:
        print("Error retrieving products.")
        return []

def display_suggestions(products):
    print("\nHere are some gift suggestions based on your answers:\n")
    for idx, product in enumerate(products, start=1):
        print(f"{idx}. {product['title']}")
        print(f"   Price: {product['price']}")
        print(f"   Link: {product['url']}")
        print("\n")

def main():
    responses = ask_questions()
    search_query = generate_search_query(responses)
    products = search_product(search_query)
    display_suggestions(products)

if __name__ == "__main__":
    main()
