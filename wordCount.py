# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 13:33:46 2018

@author: Andres Llausas
"""
import sys

file1 = sys.argv[1]
file2 = sys.argv[2]
f = open(file1, 'r')
b = open(file2, 'w+')

declaration = f.readlines()
new_declaration = []

# getting mistake due to --That, find fix for double punctuation

for line in declaration:
    temp = line.split()
    for word in temp:
        word = word.lower()
        if "-" in word and "--" not in word:
            new_words = word.split("-")
            new_declaration.append(''.join(ch for ch in new_words[0] if ch not in ";:,.()"))
            new_declaration.append(''.join(ch for ch in new_words[1] if ch not in ";:,.()"))
        elif "'" in word:
            new_words = word.split("'")
            new_declaration.append(''.join(ch for ch in new_words[0] if ch not in ";:,.()"))
            new_declaration.append(''.join(ch for ch in new_words[1] if ch not in ";:,.()"))
        else:
            new_declaration.append(''.join(ch for ch in word if ch not in ';:,.()-"'))
        
d = dict.fromkeys(sorted(new_declaration), 0)

for word in new_declaration:
    d[word] += 1
    
for key in d:
    b.write(key + ' ' + str(d[key]) + '\n')
    

f.close()
b.close()
'''
a = open('', 'r')
c = open('test_output.txt', 'r')

correct = a.readlines()
testing = c.readlines()

# result = [i for i, j in zip(correct, testing[1:]) if i != j]

print(correct == testing)
'''

