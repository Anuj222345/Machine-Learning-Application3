import streamlit as st
import pandas as pd 
from textblob import TextBlob
import emoji
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

@st.cache_data
def get_text(raw_url):
    req = Request(
        raw_url,
        headers={"User-Agent": "SentimentApp/1.0 (anuj123@gmail.com)"}
    )
    page = urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    fetched_text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return fetched_text

def main():
    """A Simple Sentiment Analysis Emoji App"""
    
    st.title("Sentiment Analysis Emoji App")
    activities = ["Sentiment", "Text Analysis of URL", "About"]
    choice = st.sidebar.selectbox("Activities",activities)
    
    
    if choice == 'Sentiment':
        st.subheader("Sentiment Analysis")
        st.write(emoji.emojize('Everyone :heart: Streamlit'))
        
        raw_text = st.text_area("Enter Text", "Type Here")
        if st.button("Analyze"):
            blob = TextBlob(raw_text)
            result = blob.sentiment.polarity
            
            
            
            if result > 0.0:
                custom_emoji = ':grinning_face_with_smiling_eyes:'
                st.write(emoji.emojize(custom_emoji))
            elif result < 0.0:
                custom_emoji = ':disappointed:'
                st.write(emoji.emojize(custom_emoji))
            else:
                st.write(emoji.emojize(':expressionless:'))
            st.info('Polarity Score::{}'.format(result))
            
            
            
            
            st.write(blob.sentiment)
            
    
    if choice == 'Text Analysis of URL':
        st.subheader("Analysis of Text from URL")
        
        raw_url = st.text_input("Enter URL", "Type Here")
        text_limit = st.slider("Length of Text to Preview",50,90)
        if st.button("Analyze"):
            if raw_url != 'Type Here':
                result = get_text(raw_url)
                blob = TextBlob(result)
                len_of_full_text = len(result)
                len_of_short_text = round(len(result)/text_limit)
                st.info("Full Text Length :: {}".format(len_of_full_text))
                st.info("Short Text Length :: {}".format(len_of_short_text))
                st.write(result[:len_of_short_text])
                
                all_sentences = [ str(sent) for sent in blob.sentences ]
                all_sentiments = [ sent.sentiment.polarity for sent in blob.sentences]
                
                
                
                new_df = pd.DataFrame(zip(all_sentences,all_sentiments), columns=["Sentences", "Sentiments"])
                st.dataframe(new_df)
                
                
                fig, ax = plt.subplots()
                new_df["Sentiments"].head(20).plot(kind='bar', ax=ax)
                ax.set_xticks([])
                st.pyplot(fig)
                
            
        
        
        
    
    
    
    
    
    
    


if __name__ == '__main__':
    main()