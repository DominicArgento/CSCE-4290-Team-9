import json
from django.http import JsonResponse
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_businesses(request):
    # Load Yelp dataset (replace 'dataset.json' with the actual file name)
    with open('path/to/dataset.json', 'r') as file:
        dataset = json.load(file)

    # Initialize sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    businesses = []
    for item in dataset:
        # Extract business information
        business_info = {
            'name': item['name'],
            'address': item['address'],
            'hours': item.get('hours', 'N/A'),
        }

        # Extract reviews and conduct sentiment analysis
        reviews = item['reviews']
        review_scores = [analyzer.polarity_scores(review)['compound'] for review in reviews]
        avg_score = sum(review_scores) / len(review_scores)

        # Determine overall rating based on sentiment score
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

        business_info['rating'] = rating

        # Create a summary of common reviews (first 50 reviews)
        common_reviews = ', '.join(reviews[:50])  # Get the first 50 reviews as summary
        business_info['summary'] = common_reviews

        businesses.append(business_info)

    return JsonResponse(businesses, safe=False)

