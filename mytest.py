import json
import re
with open("products.json") as file:
    data=json.load(file)
file.close()
last=list(data.keys())[-1]
digits=re.findall(r"\d",last) 
a=int("".join(digits))
print(a)
