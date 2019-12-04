import json


"""
Created on Wed Dec  4 16:32:51 2019

@author: Devis
"""

with open("Dylans_Movie_Data.json") as f:
    data = json.load(f)
    liked = 0
    disliked = 0
    not_seen = 0
    for movie in data:

        if movie[1]=='1':
            liked += 1
        if movie[1]=='2':
            disliked += 1
        if movie[1]=='3':
            not_seen += 1
print(liked)
print(disliked)
print(not_seen)