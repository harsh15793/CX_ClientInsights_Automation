import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm

#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('maxent_ne_chunker')
#nltk.download('words')
#nltk.download('vader_lexicon')


#st.set_page_config(page_title = 'Sentiment Analysis',
#                    page_icon = ":bar_chart:",
#                    layout = 'wide')

#st.title("Sentiment Analysis")
#st.markdown("---")

plt.style.use('ggplot')
df = pd.read_excel('files/Danske Bank .xlsx')

# Section for understanding
example = df['Review Text'][30]
tokens = nltk.word_tokenize(example)
tagged = nltk.pos_tag(tokens)
entities = nltk.chunk.ne_chunk(tagged)
#Till here

# VADER method to do the analysis
sia = SentimentIntensityAnalyzer()

res = {}
for i, row in tqdm(df.iterrows(), total=len(df)):
    text = row['Review Text']
    id = row['Id']
    res[id] = sia.polarity_scores(str(text))

vaders = pd.DataFrame(res).T
vaders = vaders.reset_index().rename(columns = {'index' : 'Id'}).merge(df, how ='left')

ax = sns.barplot(data = vaders, x = 'Stars Given', y = 'compound')
ax = ax.set_title('Compound Score By TrustPilot reviews')
plt.show()

fig, axs = plt.subplots(1,3, figsize =(15,5))
axs[0] = sns.barplot(data = vaders, x = 'Stars Given', y ='pos', ax = axs[0])
axs[0] = axs[0].set_title('Positive')
axs[1] = sns.barplot(data = vaders, x = 'Stars Given', y ='neu', ax = axs[1])
axs[1] = axs[1].set_title('neutral')
axs[2] = sns.barplot(data = vaders, x = 'Stars Given', y ='neg', ax = axs[2])
axs[2] = axs[2].set_title('Negative')
plt.show()
## VADER Analysis complete
