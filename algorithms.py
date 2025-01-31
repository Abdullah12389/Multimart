import os
import numpy as np
import pickle
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from sklearn.metrics.pairwise import cosine_similarity
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
from tensorflow.keras.utils import pad_sequences 
def similar(a,b):
    return np.linalg.matmul(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))  
def pred_next(text,how_many):
    with open("tokenizer_next_word.pkl","rb") as file:
        tokenize_next_word=pickle.load(file)
    file.close()  
    with open("next_word_pred_model.pkl","rb") as file:
        next_word=pickle.load(file)
    file.close() 
    text=text.lower()
    for i in range(how_many):
        tokens=tokenize_next_word.texts_to_sequences([text])
        pad=pad_sequences(tokens,maxlen=15,padding="pre")
        index=np.argmax(next_word.predict(pad))
        word=list(tokenize_next_word.word_index.keys())[index-1]
        text=text+" "+word
    return text
def give_sentiment(text):
    with open("tokens_review_sentiment.model","rb") as file:
        token_sentiment=pickle.load(file)
    file.close()  
    with open("review_sentiment.pkl","rb") as file:
        sentiment=pickle.load(file)
    file.close()  
    tokens=word_tokenize(text)
    lemmatize=WordNetLemmatizer()
    lemma_tokens=[lemmatize.lemmatize(word) for word in tokens]
    vector=np.mean([token_sentiment.wv[word] for word in lemma_tokens],axis=0)
    vector=np.expand_dims(np.expand_dims(vector,axis=0),axis=0)
    pred=sentiment.predict(vector)
    if pred>0.5:
        return 1
    else:
        return 0
def ChatWithMe(question):  
    with open("chatbot_tokenizer.pkl","rb") as file:
        vectorize=pickle.load(file)
    file.close()  
    sim=[]
    answers=np.load("answer_bank.npy")
    X=np.load("question_array.npy")
    text=vectorize.transform([question])
    text=text.toarray()
    for ques in X:
        sim.append(cosine_similarity(ques.reshape(1,-1),text))
    if max(sim)<0.1:
        return "I do not know about that"
    else:
        index=np.argmax(sim)
        return answers[index]


