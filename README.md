# Crypto-sentiment | ISI-Assignment

This project deals with a high level sentiment analysis of text messages from crypto.com channel in the telegram application The date range of these messages is from 1st May to 15th May, 2021

## Running the project:

Clone this repository and install the required packages by using the following command.
```sh
pip install -r requirements.txt
```

Run the python file

```sh
python main.py
```
In this project, nltk is used for filtering english words and textblob is used for sentiment analysis (since it can also give the subjectivity of messages)

Results:

![Alt text](/https://github.com/Kishan-Trivedi/Crypto-sentiment/blob/master/Crypto-plot.png "Sentiment-Analysis")

The resultant graph shows us that the sentiment during this period was mostly neutral, as the crypto market was highly volatile during this period. So the average positive sentiment and average negative sentiment was similar.
