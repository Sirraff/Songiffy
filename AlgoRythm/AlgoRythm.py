# Abstract: Converts up to 300 charaters fo text into a list of musical values

from textblob import TextBlob
import random
import os
import numpy as np

# Define the mapping between letters and notes
notes = {
    'A': 60,  # C
    'B': 62,  # D
    'C': 64,  # E
    'D': 65,  # F
    'E': 67,  # G
    'F': 69,  # A
    'G': 71,  # B
}

# Define the text to be converted into music
text = input("Type text here: ")

# Use TextBlob to determine the sentiment of the text
sentiment = TextBlob(text).sentiment.polarity

print("Sentiment is :", sentiment)

# Define the musical patterns based on sentiment
if sentiment > 0.5:
    scale = [0, 2, 4, 5, 7, 9, 11]  # major scale for positive sentiment
    pattern = [0, 2, 4, 5, 4, 2]  # pattern for positive sentiment
elif sentiment < -0.5:
    scale = [0, 2, 3, 5, 7, 8, 10]  # minor scale for negative sentiment
    pattern = [0, 3, 5, 3, 0, -2]  # pattern for negative sentiment
else:
    scale = [0, 2, 3, 5, 7, 9, 10]  # mixed scale for neutral sentiment
    pattern = [0, 2, 0, 3, 0, 2]  # pattern for neutral sentiment

print("scale: ", scale)
print("pattern: ", pattern)
