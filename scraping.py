import requests
import re
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from langdetect import detect

def scrape_url(url):
    # Make a request to the website and parse the HTML content with Beautiful Soup
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all <h1> and <p> tags in the HTML content
    headers = soup.find_all('h1')
    paragraphs = soup.find_all('p')
    
    # Extract the text from each <h1> and <p> tag and join them together
    header_contents = ' '.join([h.get_text() for h in headers])
    text_contents = ' '.join([p.get_text() for p in paragraphs])
    
    # Limit the text contents to a maximum of 3000 characters
    text_contents = text_contents[:3000]
    
    # Detect the language of the text contents
    language = detect(text_contents)
    
    # Tokenize the text contents
    words = word_tokenize(text_contents.lower())
    
    # Select the stop words based on the language of the text contents
    if language == 'en':
        stop_words = set(stopwords.words('english'))
    elif language == 'es':
        stop_words = set(stopwords.words('spanish'))
    elif language == 'de':
        stop_words = set(stopwords.words('german'))
    else:
        stop_words = set(stopwords.words('english'))
    
    # Remove stopwords from the tokenized words
    filtered_words = [word for word in words if not word in stop_words]
    
    # Join the filtered words back into a string
    cleaned_text = ' '.join(filtered_words)
    
    # Clean the text contents by removing special characters and extra whitespaces
    cleaned_text = re.sub(r'\W+', ' ', cleaned_text)
    cleaned_text = ' '.join(cleaned_text.split())
    
    return header_contents, cleaned_text
