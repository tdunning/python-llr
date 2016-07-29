from collections import Counter 
import re

import llr

def count(file):
    '''Counts the words contained in a file'''
    with open(file) as f:
        return Counter(re.findall('\w+', re.sub('[\r\n]', ' ', f.read())))

# Count words in Hamlet
hamlet = count('data/hamlet')
# and the Declaration of Independence
declaration = count('data/declaration') 

# Find out which words are used more or less
diff = llr.llr_compare(hamlet, declaration)
ranked = sorted(diff.items(), key=lambda x: x[1])

print("\nMore in Declaration of Independence")
for k,v in ranked[:10]:
    print(k, v)

print("\nMore in Hamlet")
for k,v in ranked[-10:]:
    print(k, v)
