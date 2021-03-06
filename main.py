import streamlit as st
from nltk_download_utils import * # see: https://blog.jcharistech.com/2020/12/14/deploying-nlp-apps-on-streamlit-sharing/
#nltk.download(['punkt', 'stopwords', 'tokenizers'])
#nltk.download(info_or_id="popular", download_dir="nltk")
#nltk.download('stopwords', download_dir="nltk")
import re
import sys

st.title("Text Summarizer")

intro = st.empty()
article_text = st.text_area("Provide text here")
if article_text == "":
    intro.error("Please enter text below")
else:
    st.warning("Your text")
    st.write(article_text)

    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    # Tokenization
    sentence_list = nltk.sent_tokenize(article_text) # return list of sentences; "sent" is for sentence

    # Find Weighted Frequency of Occurrence
    stopwords = nltk.corpus.stopwords.words('english')
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequency)


    # Calculating Sentence Scores
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]



    # Getting the Summary
    #nb_sentences = 7
    nb_sentences = st.number_input("enter number of sentences for summary", min_value=1,  step=1)

    import heapq
    summary_sentences = heapq.nlargest(int(nb_sentences), sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)

    st.success("Summary")
    st.write(summary)
