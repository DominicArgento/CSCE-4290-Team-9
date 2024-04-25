import json
from heapq import nlargest
from collections import Counter
import re

from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Function to load Yelp dataset 
def load_dataset(file_path):
    dataset = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            dataset.append(data)
    return dataset

# Function to search for businesses (name and zip code)
def search_businesses(dataset, name, zip_code):
    businesses_found = []
    for item in dataset:
        if name.lower() in item['name'].lower() and item['postal_code'] == zip_code:
            businesses_found.append(item)
    return businesses_found

# Function to search for reviews (business ID)
def search_reviews_by_business_id(reviews, business_id):
    return [review for review in reviews if review['business_id'] == business_id]

# Function to generate a summary of reviews (extractive summarization)
def generate_review_summary(reviews):
    # Sorted for 50 most recent reviews
    recent_reviews = sorted(reviews, key=lambda x: x['date'], reverse=True)[:50]
    
    all_text = ' '.join(review['text'] for review in recent_reviews)
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', all_text)  # Split text into sentences

    # Calculate word frequency for each sentence
    word_frequency = Counter(re.findall(r'\w+', all_text.lower()))

    # Assign a score to each sentence
    sentence_scores = {}
    for sentence in sentences:
        for word in re.findall(r'\w+', sentence.lower()):
            if word in word_frequency:
                if len(sentence.split()) < 50:  # Consider only sentences with less than 50 words
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = word_frequency[word]
                    else:
                        sentence_scores[sentence] += word_frequency[word]

    # Select top 5 sentences 
    summary_sentences = nlargest(5, sentence_scores, key=sentence_scores.get)
    return ' '.join(summary_sentences)

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

# Function to display business info
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
    
    # Count the number of reviews in each sentiment category
    sentiment_counts = Counter()
    for review in business_reviews:
        sentiment = analyze_sentiment([review])
        sentiment_counts[sentiment] += 1

    # Generate summary of reviews
    summary = generate_review_summary(business_reviews)

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
    print(f"Overall Rating: {rating}")
    print("Rating Breakdown:")
    for sentiment, count in sentiment_counts.items():
        print(f"{sentiment}: {count} review(s)")
    print("Summary of Reviews:")
    print(summary)

# Function for main menu options
def main_menu():
    print("\n1. Search for a Business")
    print("2. Exit")

def main():
    # Paths to the Yelp dataset files
    businesses_file = 'yelp_academic_dataset_business.json'
    reviews_file = 'yelp_academic_dataset_review.json'

    # Load the dataset
    businesses_data = load_dataset(businesses_file)
    reviews_data = load_dataset(reviews_file)

    while True:
        main_menu()  # Display the main menu
        choice = input("Enter your choice: ")  # Prompt the user


        if choice == '1':  
            business_name = input("Enter the name of the business: ")
            zip_code = input("Enter the zip code: ")

            # Search for businesses
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
                    display_business_details(selected_business, reviews_data) 
                else:
                    print("Invalid selection. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        elif choice == '2':  # Exit
            print("Exiting the application...")
            break

        else:  # Invalid Entry
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
