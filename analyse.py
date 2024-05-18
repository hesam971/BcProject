import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# Download NLTK VADER lexicon if not already downloaded
nltk.download('vader_lexicon')

# Load JSON data from file
with open('nameOfJsonFile', 'r') as file:
    data = json.load(file)

# Extract content from each message
contents = [message['message']['content'] for message in data]

# Initialize SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

# Analyze sentiment for each content
sentiments = []
for content in contents:
    sentiment_score = sid.polarity_scores(content)
    if sentiment_score['compound'] >= 0.05:
        sentiments.append('Positive')
    elif sentiment_score['compound'] <= -0.05:
        sentiments.append('Negative')
    else:
        sentiments.append('Neutral')

# Count the occurrences of each sentiment
sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
for sentiment in sentiments:
    sentiment_counts[sentiment] += 1

# Create a bar chart to visualize sentiment distribution
labels = sentiment_counts.keys()
values = sentiment_counts.values()

plt.bar(labels, values, color=['green', 'red', 'blue'])
plt.xlabel('Sentiment')
plt.ylabel('Frequency')
plt.title('Sentiment Analysis of Webpage')
plt.show()
