import re

text = """
Meeting on 12/09/2026
Call 9876543210
#NLP
@OpenAI
natural language processing
"""

def search(choice):
    if choice == 1:
        print(re.findall(r'\d{2}/\d{2}/\d{4}', text))

    elif choice == 2:
        print(re.findall(r'[6-9]\d{9}', text))

    elif choice == 3:
        print(re.findall(r'#\w+', text))

    elif choice == 4:
        print(re.findall(r'@\w+', text))

    elif choice == 5:
        word = input("Enter Prefix: ")
        print(re.findall(r'\b' + word + r'\w*', text))

    elif choice == 6:
        word = input("Enter Suffix: ")
        print(re.findall(r'\w*' + word + r'\b', text))

    else:
        print("Invalid Choice")

print("1.Date")
print("2.Phone")
print("3.Hashtag")
print("4.Mention")
print("5.Prefix")
print("6.Suffix")

choice = int(input("Enter Choice: "))
search(choice)
