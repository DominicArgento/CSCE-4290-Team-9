# CSCE-4290-Team-9

Team 9 Project for Natural Language Processing

**This application takes between 30 seconds to a few minutes to initialize because of the data size**

This is a project aimed at helping understand the overall sentiment of a certain business within Yelp's dataset. The application asks the user for a business name and then prompts for its corresponding zip code. It then analyzes reviews and provides business information, as well as overall sentiment based on that score (a breakdown is provided) and a summary of the previous 50 reviews (this is based on word frequency and sentence score).

The main Python file is in Yelp_Sentiment. Users will still have to download NLTK's VADER lexicon (it is provided in its own Python file, navigate to file location in terminal, run 'python download_nltk.py'), as well as download, unzip, and add in the two supporting dataset JSON files (yelp_academic_dataset_review AND yelp_academic_dataset_business) to the application's file location. (Files are too big for GitHub(even if zipped!!), one is 8GB alone)
dataset URL: https://www.yelp.com/dataset/download 
