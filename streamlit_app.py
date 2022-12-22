import plotly.express as px
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

keywords = ['service','payment','customer experience','support']

st.set_page_config(page_title = 'Customer Experience', layout='wide')
st.title("Customer Sentiment Analyzer")
selected_company = st.selectbox("Select the Company:",options = ['U.S. Polo Assn','Danske Bank'])
selected_keyword = st.selectbox("Select the Keyword:",options = keywords)
st.markdown("---")
st.header(f"{selected_company} Sentiments for '{selected_keyword}'")

df =''

if(selected_company == 'U.S. Polo Assn'):
    df = pd.read_excel('files/U.S. Polo Assn_sentiments.xlsx')
elif (selected_company == 'Danske Bank'):
    df = pd.read_excel('files/Danske Bank_sentiments.xlsx')

for keyword in keywords:
    df[keyword] = 0

#text_for_wordcloud = ""

for keyword in keywords:
    for index,row in df.iterrows():
        #text_for_wordcloud = text_for_wordcloud + " " + str(row['Review Text'])
        if str(row['Review Heading']).find(keyword) != -1 or str(row['Review Text']).find(keyword) != -1:
            df.at[index,keyword] = 1
#st.dataframe(df)


value_neg = 0
value_pos = 0
value_nue = 0
count = 0

for index,row in df.iterrows():
    if(df.at[index,selected_keyword] == 1):
        value_neg = value_neg + row["roberta_neg"]
        value_pos = value_pos + row["roberta_pos"]
        value_nue = value_nue + row["roberta_neu"]
        count = count + 1
average_neg = value_neg/count
average_pos = value_pos/count
average_nue = value_nue/count
#st.write(f"Average Negative sentiment for {keyword} is {average_neg}")
#st.write(f"Average Positive sentiment for {keyword} is {average_pos}")
#st.write(f"Average Neutral sentiment for {keyword} is {average_nue}")
fig1 = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = average_neg,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': f"Negative Sentiment"},
    gauge = {'axis': {'range': [0, 1]},'bar': {'color': "black"},
             'steps' : [
                 {'range': [0, 0.4], 'color': "yellow"},
                 {'range': [0.4, 0.7], 'color': "orange"},
                 {'range': [0.7, 1], 'color': "red"}]}))

fig2 = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = average_pos,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': f"Positive Sentiment"},
    gauge = {'axis': {'range': [0, 1]},'bar': {'color': "black"},
             'steps' : [
                 {'range': [0, 0.4], 'color': "yellow"},
                 {'range': [0.4, 0.7], 'color': "lightgreen"},
                 {'range': [0.7, 1], 'color': "darkgreen"}]}))

left,right = st.columns(2)
with left:
    st.plotly_chart(fig1)
with right:
    st.plotly_chart(fig2)


#stopwords = STOPWORDS
#wc = WordCloud(background_color = 'white', stopwords = stopwords)
#wc.generate(text_for_wordcloud)
#plt.imshow(wc, interpolation = 'bilinear')
#plt.axis("off")
#plt.show()
#st.pyplot()


#plot = px.treemap(data_frame = df, path=['Stars Given'], color='roberta_neg', color_continuous_scale = 'burgyl')
#st.plotly_chart(plot)
