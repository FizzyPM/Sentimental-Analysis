import re
import nltk
import emoji
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')


def remove_stopwords(tweet):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(tweet)
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    return filtered_sentence


def handle_emojis(tweet):
    # Smile -- :), : ), :-), (:, ( :, (-:, :')
    tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' :smiley: ', tweet)
    # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
    tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' :laugh: ', tweet)
    # Love -- <3, :*
    tweet = re.sub(r'(<3|:\*)', ' :love: ', tweet)
    # Wink -- ;-), ;), ;-D, ;D, (;,  (-;
    tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' :wink: ', tweet)
    # Sad -- :-(, : (, :(, ):, )-:
    tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' :sad: ', tweet)
    # Cry -- :,(, :'(, :"(
    tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' :cry: ', tweet)
    # Handling other emojis
    tweet = emoji.demojize(tweet)
    return tweet


def preprocess_tweet(tweet):
    # Convert to lower case
    tweet = tweet.lower()
    # Removing non-ASCII characters
    # tweet = ''.join(i for i in tweet if ord(i) < 128)
    # Replace the URLs to empty strings
    tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', '', tweet)
    # Replace @handle with the empty string
    tweet = re.sub(r'@[\S]+', '', tweet)
    # Replaces #hashtag with hashtag
    tweet = re.sub(r'#(\S+)', r' \1 ', tweet)
    # Remove RT (retweet)
    tweet = re.sub(r'\brt\b', '', tweet)
    # Replace 2+ dots with space
    tweet = re.sub(r'\.{2,}', ' ', tweet)
    # Replace emojis with their type
    tweet = handle_emojis(tweet)
    # Strip space, " and ' from tweet
    tweet = tweet.strip(' "\'')
    # Replace multiple spaces with a single space
    tweet = re.sub(r'\s+', ' ', tweet)
    # funnnnny --> funny
    tweet = re.sub(r'(.)\1+', r'\1\1', tweet)
    # Removing punctuations
    tweet = re.sub(r'[^\w\s]', '', tweet)
    # Removing numbers
    tweet = re.sub("^\d+\s|\s\d+\s|\s\d+$", ' ', tweet)
    return tweet


def replace_slang(text):
    with open('slangs.txt') as file:
        slang_map = dict(map(str.strip, line.partition('\t')[::2]) for line in file if line.strip())
    for word in text.split():
        if word in slang_map.keys():
            return (text.replace(word, slang_map[word]))


# def expandContractions(text):
#     cList = {
#         "ain't": "am not", "aren't": "are not", "can't": "cannot", "'cause": "because", "could've": "could have", "couldn't": "could not", "didn't": "did not", "doesn't": "does not", "don't": "do not", "hadn't": "had not", "haven't": "have not", "he'd": "he would", "he'll": "he will",
#         "he's": "he is", "how'd": "how did", "how'll": "how will", "how's": "how is", "I'd": "I would", "I'll": "I will", "I'm": "I am", "I've": "I have", "isn't": "is not", "it'd": "it had", "it'll": "it will", "it's": "it is", "let's": "let us", "ma'am": "madam", "mayn't": "may not",
#         "might've": "might have", "mightn't": "might not", "must've": "must have", "mustn't": "must not", "needn't": "need not", "o'clock": "of the clock", "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not", "she'd": "she would", "she'll": "she will", 
#         "she's": "she is", "should've": "should have", "shouldn't": "should not", "so've": "so have", "so's": "so is", "that'd": "that would", "that's": "that is", "there'd": "there had", "there's": "there is", "they'd": "they would", "they'll": "they will", "they're": "they are", 
#         "they've": "they have", "to've": "to have", "wasn't": "was not", "we'd": "we had", "we'll": "we will", "we're": "we are", "we've": "we have", "weren't": "were not", "what'll": "what will", "what're": "what are", "what's": "what is", "what've": "what have", "when's": "when is", 
#         "when've": "when have", "where'd": "where did", "where's": "where is", "where've": "where have", "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have", "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not", 
#         "won't've": "will not have", "would've": "would have", "wouldn't": "would not", "y'all": "you all", "y'alls": "you alls", "you'd": "you had", "you'll": "you you will", "you're": "you are", "you've": "you have"}
#     c_re = re.compile('(%s)' % '|'.join(cList.keys()))

#     def replace(match):
#         return cList[match.group(0)]
#     return c_re.sub(replace, text)


df = pd.read_table('./datasets/test-A-input.txt', sep='\t', names=('A', 'B', 'C', 'D', 'E', 'F'))
# f = open("preprocessed-A.txt", "w")
# print(df.head())
# print(df.iloc[:, 5])
for row in (df.iloc[:, 5].head()):
    if (row != 'Not Available'):
        row = replace_slang(row)
        # row = expandContractions(row)
        row = preprocess_tweet(row)
        row = remove_stopwords(row)
        print(row)
