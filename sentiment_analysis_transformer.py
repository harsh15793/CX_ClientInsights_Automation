import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import xlsxwriter
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
from tqdm.notebook import tqdm

MODEL = f'cardiffnlp/twitter-roberta-base-sentiment'
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

plt.style.use('ggplot')
#df = pd.read_excel('files/Danske Bank .xlsx')
#workbook = xlsxwriter.Workbook('files/Danske Bank_sentiments.xlsx')
df = pd.read_excel('files/U.S. Polo Assn. .xlsx')
workbook = xlsxwriter.Workbook('files/U.S. Polo Assn_sentiments.xlsx')
workbook.close()

def polarity_ratings_roberta(example):
    encoded_text = tokenizer(example, return_tensors ='pt')
    output = model(**encoded_text)
    ratings = output[0][0].detach().numpy()
    ratings = softmax(ratings)
    ratings_dict = {
        'roberta_neg' : ratings[0],
        'roberta_neu' : ratings[1],
        'roberta_pos' : ratings[2]
    }

    return ratings_dict
res ={}
for i, row in tqdm(df.iterrows(), total=len(df)):
    try:
        text = row['Review Text']
        id = row['Id']
        res[id] = polarity_ratings_roberta(str(text))
    except:
        print(f'Broke for row {id}')

results_df = pd.DataFrame(res).T
results_df = results_df.reset_index().rename(columns = {'index' : 'Id'}).merge(df, how ='left')

with pd.ExcelWriter('files/U.S. Polo Assn_sentiments.xlsx',mode="a",engine="openpyxl",if_sheet_exists="overlay") as writer:
    results_df.to_excel(writer, sheet_name="Sheet1",index=False)

fig = sns.pairplot(data = results_df,
            vars =['roberta_neg', 'roberta_neu', 'roberta_pos'],
            hue = 'Stars Given',
            palette = 'tab10')
#plt.show()

#Example to check for wrongly assessed comments
#print(results_df.query('`Stars Given` == 1').sort_values('roberta_pos', ascending = False)['Review Text'].values[0])
#fig = plt.figure()
#st.pyplot(fig)
