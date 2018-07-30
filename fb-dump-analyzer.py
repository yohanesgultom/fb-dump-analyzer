"""
Analyze facebook dump json data. How to download your data https://www.facebook.com/help/1701730696756992?helpref=hc_global_nav

@author yohanes.gultom@gmail.com
"""

import argparse
import os
import json
import matplotlib.pyplot as plt
import collections
import nltk
import numpy as np
from pprint import pprint
from datetime import datetime

IGNORE_TOKENS = [ 'but', 'me', 'karena', 'buat', 'kita', 'my', 'they', 'your', 'ya', 'saya', 'i', 'we', 'you', '~', 'sudah', 'mau', 'banyak', 'http', 'https', '@', 'kalau', 'do', 'or', 'saat', 'punya', 'selalu', 'adalah', 'sama', 'was', "n't", 'so', 'saja', 'at', 'tapi', 'this', 'has', 'by', 'bukan', 'have', 'no', 'via', 'as', 'will', 'atau', 'harus', 'an', 'dalam', 'are', 'lagi', 'lebih', '--','akan', 'v', 'jadi', 'can', "'s", 'ada', 'not', 'juga', 'ke', 'with', 'the', 'dengan', 'on', 'bisa', 'be', 'that', 'itu', 'dari', 'it', '#', 'for', '!', 'untuk', 'in', 'ini', 'tidak', '&', 'di', 'd', '?', 'is', 'and', 'a', 'of', 'dan','``', "''", 'to', 'the', ')', '(', 'yang', ':', '.', ',']

# download punkt resource if not yet available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# parse args
parser = argparse.ArgumentParser()
parser.add_argument("input_dir", help="Facebook dump (json) root directory")
args = parser.parse_args()

# parse posts
posts_file = os.path.join(args.input_dir, "posts", "your_posts.json")
f = open(posts_file, "r")
data = json.load(f)

total_posts = len(data["status_updates"])
total_posts_year = collections.OrderedDict()
token_counts_per_year = collections.OrderedDict()
for status in data["status_updates"]:
    dt = datetime.fromtimestamp(status["timestamp"])
    total_posts_year[dt.year] = 1 if dt.year not in total_posts_year else total_posts_year[dt.year] + 1
    if "data" in status:
        # no data contains more than one item
        tokens = nltk.word_tokenize(status["data"][0]["post"])
        if dt.year not in token_counts_per_year:
            token_counts_per_year[dt.year] = {}            
        for token in tokens:
            token = token.lower()
            if token not in IGNORE_TOKENS:
                token_counts_per_year[dt.year][token] = 1 if token not in token_counts_per_year[dt.year] else token_counts_per_year[dt.year][token] + 1

# plot posts stats
years = total_posts_year.keys()
posts = total_posts_year.values()
plt.figure(1)
plt.plot(years, posts)
plt.xlabel('Year')
plt.ylabel('Total Posts')
plt.title('Annual Facebook Posts')

# plot top tokens on top year
max_post_year = max(total_posts_year.keys(), key=(lambda key: total_posts_year[key]))
sorted_by_value = sorted(token_counts_per_year[max_post_year].items(), key=lambda kv: kv[1], reverse=True)
top = 20
tokens = [token for token, count in sorted_by_value[top::-1]]
counts = [count for token, count in sorted_by_value[top::-1]]
plt.figure(2)
plt.barh(tokens, counts)
plt.xlabel('Token')
plt.ylabel('Count')
plt.suptitle('Top {} token in {}'.format(top, max_post_year))
plt.title('Meaningless tokens (sym, pron, prep, conj .etc) removed', fontsize=7)

plt.show()