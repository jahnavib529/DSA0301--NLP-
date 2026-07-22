from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
text = input("Enter text: ")
words = word_tokenize(text)
result = [w for w in words if w.lower() not in stopwords.words('english')]
print(result)
