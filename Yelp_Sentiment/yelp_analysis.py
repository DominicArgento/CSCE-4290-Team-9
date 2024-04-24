import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Function to load the Yelp dataset from a JSON file
def load_dataset(file_path):
    dataset = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            dataset.append(data)
    return dataset

# Function to search for businesses by name and zip code
def search_businesses(dataset, name, zip_code):
    businesses_found = []
    for item in dataset:
        if name.lower() in item['name'].lower() and item['postal_code'] == zip_code:
            businesses_found.append(item)
    return businesses_found

# Function to search for reviews by business ID
def search_reviews_by_business_id(reviews, business_id):
    return [review for review in reviews if review['business_id'] == business_id]

# Function to analyze the sentiment of reviews and determine the overall rating
def analyze_sentiment(reviews):
    analyzer = SentimentIntensityAnalyzer()
    review_scores = [analyzer.polarity_scores(review['text'])['compound'] for review in reviews]
    avg_score = sum(review_scores) / len(review_scores)
    if avg_score < -0.6:
        rating = "Very Bad"
    elif avg_score < -0.2:
        rating = "Bad"
    elif avg_score < 0.2:
        rating = "Okay"
    elif avg_score < 0.6:
        rating = "Good"
    else:
        rating = "Very Good"
    return rating

# Function to display detailed information about a selected business
def display_business_details(business, reviews):
    business_id = business['business_id']
    name = business['name']
    address = business['address']
    city = business['city']
    state = business['state']
    postal_code = business['postal_code']
    hours = business['hours'] if 'hours' in business else None
    categories = business['categories'].split(', ') if 'categories' in business else None
    business_reviews = search_reviews_by_business_id(reviews, business_id)

    # Analyze sentiment of reviews
    rating = analyze_sentiment(business_reviews)

    # Display business details
    print("\nBusiness Details:")
    print(f"Business ID: {business_id}")
    print(f"Name: {name}")
    print(f"Address: {address}, {city}, {state} {postal_code}")
    if hours:
        print("Hours:")
        for day, timings in hours.items():
            print(f"  {day}: {timings}")
    if categories:
        print("Categories:", ', '.join(categories))
    print(f"Rating: {rating}")
    print("Reviews:")
    for idx, review in enumerate(business_reviews[:3]):  # Display only the first 3 reviews
        print(f"Review {idx + 1}: {review['text']}")

# Function to display the main menu options
def main_menu():
    print("\n1. Search for a Business")
    print("2. Exit")

# Main function to run the application
def main():
    # Paths to the Yelp dataset files
    businesses_file = 'yelp_academic_dataset_business.json'
    reviews_file = 'yelp_academic_dataset_review.json'

    # Load the dataset
    businesses_data = load_dataset(businesses_file)
    reviews_data = load_dataset(reviews_file)

    while True:
        main_menu()  # Display the main menu
        choice = input("Enter your choice: ")  # Prompt the user for choice

        if choice == '1':  # If the user chooses to search for a business
            business_name = input("Enter the name of the business: ")
            zip_code = input("Enter the zip code: ")

            # Search for businesses with the specified name and zip code
            businesses = search_businesses(businesses_data, business_name, zip_code)

            if not businesses:
                print("No businesses found with the specified name and zip code.")
                continue

            print("\nBusinesses found:")
            for idx, business in enumerate(businesses, start=1):
                print(f"{idx}. {business['name']}")

            selected_idx = input("\nEnter the number of the business to view details (0 to cancel): ")
            if selected_idx == '0':
                continue

            try:
                selected_idx = int(selected_idx)
                if 1 <= selected_idx <= len(businesses):
                    selected_business = businesses[selected_idx - 1]
                    display_business_details(selected_business, reviews_data)  # Display details of the selected business
                else:
                    print("Invalid selection. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        elif choice == '2':  # If the user chooses to exit
            print("Exiting the application...")
            break

        else:  # If the user enters an invalid choice
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
