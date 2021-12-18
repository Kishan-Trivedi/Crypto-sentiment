import json
import re
from collections import defaultdict
from statistics import mean

import nltk
import plotly.graph_objects as go
import tqdm
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from plotly.subplots import make_subplots
from textblob import TextBlob
from tqdm import tqdm

nltk.download('words')
nltk.download('stopwords')
nltk.download('wordnet')

words = set(nltk.corpus.words.words())
words.add('DOGE')
words.add('SHIB')
words.add('shib')
words.add('doge')
words.add('dogecoin')
words.add('shibcoin')

stop_words = set(stopwords.words('english'))

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


def filter_english_words(message):
    result = " ".join(lemmatizer.lemmatize(stemmer.stem(w)) for w in nltk.wordpunct_tokenize(message) if
                      (w.lower() in words and w not in stop_words) or not w.isalpha())
    return result


def read_telegram_file(path):
    data_dict = defaultdict(list)
    with open(path, "r", encoding="utf-8") as read_file:
        data = json.load(read_file)
        for message in tqdm(data['messages'], desc='Reading the telegram file'):
            message_date = message['date'][0:10]
            text_message = message['text']
            if type(text_message) is list:
                flattened_message = ''
                for i in range(len(text_message)):
                    if type(text_message[i]) is str:
                        flattened_message += (text_message[i])
                    else:
                        flattened_message += (text_message[i]['text'])
                data_dict[message_date].append(clean_data(flattened_message))
            else:
                data_dict[message_date].append(clean_data(text_message))
        return data_dict


def clean_data(input_message):
    # remove whitespace
    input_message = input_message.strip()
    # lowercase
    input_message = input_message.lower()
    # remove numbers
    input_message = re.sub(r'\d+', '', input_message)
    return input_message


def plot_graph():
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=list(number_of_messages.keys()), y=list(number_of_messages.values()), name="Number-Of-Messages"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=list(sentiment_dict.keys()), y=list(sentiment_dict.values()), name="Average-Sentiment"),
        secondary_y=True,
    )
    fig.update_layout(
        title_text="Crypto-Sentiment"
    )
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Number-Of-Messages", secondary_y=False)
    fig.update_yaxes(title_text="Average-Sentiment", secondary_y=True)
    fig.show()


if __name__ == "__main__":
    filtered_messages = defaultdict(list)
    sentiment_dict = defaultdict(float)
    number_of_messages = defaultdict(int)
    telegram_data = read_telegram_file("result.json")

    for date, list_of_messages in tqdm(telegram_data.items(), desc='Filtering english messages'):
        for sentence in list_of_messages:
            if 'DOGE' in sentence or 'SHIB' in sentence or 'doge' in sentence or 'shib' in sentence:
                filtered_messages[date].append(TextBlob(filter_english_words(sentence)).sentiment[0])

    for date, list_sentiment in tqdm(filtered_messages.items(), desc='Plotting the graph'):
        sentiment_dict[date] = mean(list_sentiment)
        number_of_messages[date] = len(list_sentiment)

    plot_graph()
