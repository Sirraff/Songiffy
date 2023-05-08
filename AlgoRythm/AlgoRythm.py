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

def get_scale_and_pattern(sentiment):
    if sentiment > 0.7:
        scale = [0, 2, 4, 5, 7, 9, 11]  # major scale for very positive sentiment
        pattern = random.choices([0, 2, 4, 5, 4, 2], k=10)  #randomly chooses 10 notes from the major scale
    elif sentiment > 0.3:
        scale = [0, 2, 4, 5, 7, 9, 10]  # mixed scale for positive sentiment
        pattern = random.choices([0, 2, 4, 5, 4, 2], k=10)  #randomly chooses 10 notes from the mixed scale
    elif sentiment > -0.3:
        scale = [0, 2, 3, 5, 7, 9, 10]  # mixed scale for neutral sentiment
        pattern = random.choices([0, 2, 0, 3, 0, 2], k=10)  #randomly chooses 10 notes from the mixed scale
    elif sentiment > -0.7:
        scale = [0, 2, 3, 5, 6, 8, 10]  # sad scale for negative sentiment
        pattern = random.choices([0, -2, -3, -2, 0, -2], k=10)  #randomly chooses 10 notes from the sad scale
    else:
        scale = [0, 2, 3, 5, 7, 8, 10]  # minor scale for very negative sentiment
        pattern = random.choices([0, -3, -5, -3, 0, 2], k=10)  #randomly chooses 10 notes from the angry scale 
    return scale, pattern

# Get the scale and pattern based on sentiment
scale, pattern = get_scale_and_pattern(sentiment)

print("Sentiment is :", sentiment)
print("scale: ", scale)
print("pattern: ", pattern)
