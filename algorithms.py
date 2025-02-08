import numpy as np
import pickle
import json
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np
import onnxruntime as rt
import io
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
def similar(a,b):
    return np.linalg.matmul(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))  
def pred_next(text,how_many):
    with open("tokenz_next_word.json") as file:
        tokenizer=json.load(file)
    file.close()
    text=text.lower()
    model=rt.InferenceSession("next_word.onnx",providers=["CPUExecutionProvider"])
    for i in range(how_many):
        tokens=[tokenizer[token] for token in text.split() if token in tokenizer.keys()]
        length=len(tokens)
        if length<=14:
            paded=np.pad(tokens,(14-length,0))
        else:
            paded=tokens[:14]
        index=np.argmax(model.run(['dense'],{"input":np.expand_dims(paded.astype(np.int32),axis=0)}))
        word=list(tokenizer)[index+1]
        text=text+" "+word
    return text
def give_sentiment(text):
    model=rt.InferenceSession('sentiment_analysis.onnx',providers=['CPUExecutionProvider'])
    with open("sentiment_tokens.json") as file:
        tokenizer=json.load(file)
    file.close()    
    tokens=word_tokenize(text)
    lemmatize=WordNetLemmatizer()
    lemma_tokens=[lemmatize.lemmatize(word) for word in tokens]
    vector=[tokenizer[word] for word in lemma_tokens if word in tokenizer.keys()]
    if len(vector)<=100:
        paded=np.pad(vector,(100-len(vector),0))
    else:
        paded=np.array(vector[:100])    
    vector=np.expand_dims(paded,axis=0)
    try:
        pred=model.run(['dense_32'],{"input":vector})
    except Exception as e:
        return 0    
    if pred[0][0][0]>0.5:
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
def tell_vernelable(img):
    model=rt.InferenceSession("vernelable_detect.onnx",providers=['CPUExecutionProvider'])
    pred=model.run(['dense_2'],{"input":img})
    if pred[0][0][0]>0.5:
        return 1
    else:
        return 0 

   

