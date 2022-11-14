from transformers import pipeline

#just trying out a new method
# not for the project
sent_pipeline = pipeline('sentiment-analysis')

print(sent_pipeline("Bank customer care is pathetic"))
