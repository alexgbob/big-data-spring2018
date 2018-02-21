# Problem Set 1: Intro to Python

## A. Lists
#A.1 Create a list containing any 4 strings
l1 = ["chaco", "Santitas", "Kris", "Doug"]
#A.2 Print the 3rd item in the list
print(l1[2])
#A.3 Print the 1st and 2nd item in the list
print(l1[0:2])
# A.4 Add a new string with text “last” to the end of the list and print the list
l1.append("last")
print(l1)
#A.5 Get the list length and print it
print(len(l1))
#A.6 Replace the last item in the list with the string “new” and print
l1[4] = "new"
print(l1)

## B. strings

sentence_words = ['I', 'am', 'learning', 'Python', 'to', 'munge', 'large', 'datasets', 'and', 'visualize', 'them']
#B.1 Convert the 'sentence_words' into a normal sentence
sentnc = str.join(" ", sentence_words)
print(sentnc,".") #can't forget your punctuation!
#B.2 Reverse the order of 'sentence_words'
sentence_words.reverse()
print(sentence_words)
#B.3 sort sentence words using defaut sorting methods
sentence_words.sort()
print(sentence_words)
#B.4 Sort using the sorted() function
sorted(sentence_words) #sorted sorts the list without modifying the ordering of the original list object. .sort reorder the items of the list object.
#B.5 Sort alphabetically without sorting by case
sentence_words.sort(key=lambda s: s.lower())
print(sentence_words)

# C Random Function

from random import * #import random module

def random_int(high_num,low_num = 0): #define random_int function with parameter high_num and low_num and low_num defaulting to 0
    num = randint(low_num, high_num) #define variable num that is a random integer between low_num and high_num inclusive
    return(num) #return num to user

# test with assert function ## the error that is returned seems to be something wrong with the <= in the given assert lines.
assert(0 <= random_int(100) <= 100)
assert(50 <= random_int(100, low_num = 50) <= 100)

# D String formating function

def pswd_eval():
    password = input("input password -->")
    sp_char = ['!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=']
    if len(str(password)) < 8:
        message = "password too short"
    elif len(str(password)) > 14:
        message = "password too long"
    elif sum(i.isdigit() for i in password) < 2:
        message = "password must include at least 2 digit"
    elif sum(i.isupper() for i in password) < 1:
        message = "passowrd must include at least 1 uppercase letter"
    elif sum(i in sp_char for i in password) < 1:
        message = "passowrd must include at least 1 character from this list: ['!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=']"
    else:
        message = "Great password!"
    return(message)

# F. Exponentiation Function

def exp(base,exponent):
    result = base
    if exponent == 0:
        result = 1
    while exponent > 1:
        result = result * base
        exponent = exponent - 1
    return result


# G. Extra Credit: Min and Max Functions

# Min Function

def min(*numeric_list):
    minimum = sorted(numeric_list)
    return minimum[0]

# Test
numeric_list = 100, 599, 11111, 3, 9
num_items = len(numeric_list)
num_items

#Max Function

def max(*numeric_list):
    num_items = len(numeric_list)
    maximum = reversed(numeric_list.sort())
    return maximum[0]

# test
max(100, 599, 11111, 3, 9)
