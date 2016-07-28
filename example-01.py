from collections import Counter 
import re

import llr

def count(file):
    with open(file) as f:
        return Counter(re.findall('\w+', re.sub('[\r\n]', ' ', f.read())))

hamlet = count('data/hamlet')
declaration = count('data/declaration') 

diff = llr.llr_compare(hamlet, declaration)

print("\nMore in Declaration of Independence")
for k,v in sorted(diff.items(), key=lambda x: x[1])[:10]:
    print(k, v)

print("\nMore in Hamlet")
for k,v in sorted(diff.items(), key=lambda x: x[1])[-10:]:
    print(k, v)
