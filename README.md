this is a modeule for sentiment classification.

1 - oftware requirement:
1.1 install the followning libraries using pip (pandas, numpy, nltk {corpus, tokenizer, stem}, scikit-learn, re, jolib)
1.2 Data must have the following attributes (text, aspect, x, y):
    text: is the text be to classified
    aspect: i.e. the company to checked
    x, y: the location where date was published
1.3 the return type is a data frame with (aspect, x, y, sentiment)

2 - user manuale
just import the sentiment_classifier and pass it the data frame import using the following line from Modules.utils import sentiment_clossifier, also not that the Modules must be in the same directory as your source file or change the path
or just run the run.sh or run.bat in your terminal and provide it with the x, y, aspect, text, data to be classified as csv and the  output path and file name with csv format
3-available algorithms:
    3.1:support vector machine classifier with linear kernel.
    vectorizer used is tf-idf vectorizer
    
4-QGIS plugin(geo_sentiment):
	load the csv file use the delimited text blugin
	2-the plugin is easy to use all you have to do is just activate one layer which has the data you just loaded the click the blugin and press 		the go button and the magic happens
