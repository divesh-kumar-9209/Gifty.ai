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
    # Using .get() to avoid KeyErrors, with defaults in case of missing data
    recipient = responses.get('Who are you buying the gift for?', 'someone')
    occasion = responses.get('What’s the occasion?', 'any occasion')
    interests = responses.get('What are some of their interests?', 'general interests')
    
    query = f"{recipient} gift for {occasion} {interests}"
    return query
def search_product(query):
    # Mock data for testing purposes
    mock_products = [
        {"title": "Personalized Mug", "price": "$15.00", "url": "https://example.com/mug"},
        {"title": "Leather Wallet", "price": "$30.00", "url": "https://example.com/wallet"},
        {"title": "Handmade Scarf", "price": "$25.00", "url": "https://example.com/scarf"}
    ]
    return mock_products
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
