"""
auther: Jack M. Isaac
e-mail: jackmahfouz766@gmail.com
date of update : apr 29 2023
version 1.0.0
"""
##############################
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import joblib
import geopandas as gpd
from shapely.geometry import Point
############ functional preprocessing logic#################

lemmatizer = WordNetLemmatizer()
vectorizer = TfidfVectorizer()

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

def to_lower(data):
    return str(data).lower()

def at_remover(data):
    return str(data).replace("@", "")

def url_remover(data):
    return re.sub(r"\S*https?:\S*", "", data)

def spacer(data):
    return re.sub("\s+", " ", data)

def punc_remover(data):
    return re.sub(r'[^\w\s]','',data)

def num_remover(data):
    return re.sub("^\d+\s|\s\d+\s|\s\d+$", "", data)

def tokenizer_and_stopwords(data):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(data)
    return [w for w in word_tokens if not w.lower() in stop_words]


def lemmatization(data):
    lem = []
    for word in data:
        lem.append(lemmatizer.lemmatize(word))
    return lem

def string_joiner(data):
    return ' '.join(data)

vectorizer = joblib.load("Modules/vectorizer.sav") 

def Attributer(dataframe, text="text"):
    """_summary_

    Args:
        dataframe (_pd.DataFrame_): _data frame_
        must contain a text attribute which will be preprocessed
    Returns:
        _pd.sparce_matrix_
    """
    dataframe[text] = dataframe[text].apply(remove_emojis)
    dataframe[text] = dataframe[text].apply(to_lower)
    dataframe[text] = dataframe[text].apply(at_remover)
    dataframe[text] = dataframe[text].apply(url_remover)
    dataframe[text] = dataframe[text].apply(spacer)
    dataframe[text] = dataframe[text].apply(punc_remover)
    dataframe[text] = dataframe[text].apply(num_remover)
    dataframe[text] = dataframe[text].apply(tokenizer_and_stopwords)
    dataframe[text] = dataframe[text].apply(lemmatization)
    dataframe[text] = dataframe[text].apply(string_joiner)
    return vectorizer.transform(dataframe.text)

svm_model = joblib.load("Modules/svm_Sentiment_classifier.sav")

def sentiment_clossifier(path, aspect, text="text", x_coord="x", y_coord="y"):
    sentiment_frame = pd.DataFrame()
    data_frame = pd.read_csv(path)
    data_frame.dropna(inplace=True)
    sentiment_frame[aspect], sentiment_frame[x_coord], sentiment_frame[y_coord]  = data_frame[aspect], data_frame[x_coord], data_frame[y_coord]
    X = Attributer(data_frame, text)
    sentiment_frame["sentiment"] = svm_model.predict(X)
    return sentiment_frame

def df_to_shp(df : pd.DataFrame,  outpath, filename, x="x", y="y"):
    geometry = [Point(xy) for xy in zip(df[x], df[y])]
    gdf = gpd.GeoDataFrame(df, crs='EPSG:4326', geometry=geometry)
    gdf.to_file(outpath+filename, driver='ESRI Shapefile')