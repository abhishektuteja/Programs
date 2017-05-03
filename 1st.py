# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

a = 10
print ("a=10")
2+2
squares = [1, 4, 9, 16, 25]
print squares [-1]
print squares [-2]

a,b, c = 0, 1, 0
while c < 10:
        print (b)
        a, b, c = b, a+b, c+1
        
print (all ([]))
print (any ([]))

from collections import defaultdict, Counter

dict1 = {}
dict1["One"] = 1
dict1 ["Two"] = 2
print (dict1)
def sum_product (a,b):
    return a+b, a*b
one = sum_product (dict1["One"], dict1["Two"])
print (one)
print (squares)
# i_list=[x for x in squares if x <5]
#print (i_list)
print ([x for x in squares if x <5])
a= raw_input("Enter something:")
print (a)

a = input ("Enter something:")
print (a)
i=0
from matplotlib import pyplot as plt
movies = [" Annie Hall", "Ben-Hur", "Casablanca", "Gandhi", "West Side Story"] 
num_oscars = [5, 11, 3, 8, 10] 
# bars are by default width 0.8, so we'll add 0.1 to the left coordinates 
# so that each bar is centered 
xs = [i + 0.5 for i, _ in enumerate( movies)] 
# plot bars with left x-coordinates [xs], heights [num_oscars] 
plt.bar( xs, num_oscars) 
plt.ylabel("# of Academy Awards") 
plt.title(" My Favorite Movies") 
# label x-axis with movie names at bar centers 
plt.xticks([ i+0.5 for i, _ in enumerate( movies)], movies) 
plt.show()

name = raw_input ("What's your name:")
print (str(name))
# Add check if it is only string and two parts first name followed by surname
Age = raw_input ("What's your age:")
# Add check if it is between 0 and 100 and not a non-numeral
print (Age)
print ( "Hi " + str(name) + " !! You will be 100 years of age in Year: " + str(2117 - int(Age)))

import sys
dir(sys)

race = 'day'
print (type(race))
print (race, 'is ' + str(type (race)))


def sum_double(a, b):
  if (a!=b):
    return (a+b)
  else
    return (2* (a+b))


str = ' bad'

if str.startswith('not', 0):
    print (str)
else:
    print ('not ' + str)

def missing_char(str1, n):
  l = -1
  str_new = ""
  list_new = list(str1)
  for j in str1:
    l = l+1
    if (l ==n):
        continue
    str_new= str_new + j
    print str_new
    
  return str_new

missing_char ('kitten', 3)

def front_back(str):
  list_new = list (str)
  a = list_new [0]
  list_new [0] = list_new[-1]
  list_new[-1] = a
  return (''.join(list_new))

front_back('a')


import MySQLdb

db = MySQLdb.connect("localhost","root","MS1@gotit","mydb" )

cursor = db.cursor()

activate python36

import tweepy

auth = tweepy.OAuthHandler('OGu9A5fnDqudVPCcgjhIeJsYs', '2SqqGeGiEVRMNKbqlBbwUW0qcSUOAUDudYyTeny6qh3tr4P3xw')
auth.set_access_token('857599922006315009-4R47ip506Jeju2zw5ORvJXOZzS78Huv', '8zJteuYlhkyAFSfoM3P61HDJ6lI2gXDpx3ZimpLKELR75')

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print (tweet.text)