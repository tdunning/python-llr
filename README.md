# Python LLR

This project contains a python implementation of the most
commonly used variants of the G-test. To learn more about the test
itself check out
[my blog on LLR tests](http://tdunning.blogspot.com/2008/03/surprise-and-coincidence.html),
[the original paper on using LLR for linguistics](http://aclweb.org/anthology/J93-1003),
the
[wikipedia article on multinomial LLR tests](https://en.wikipedia.org/wiki/G-test)
or [my dissertation](http://arxiv.org/abs/1207.1847)

If you have problems, you can add a comment to the blog mentioned
above, or raise an issue on this github repo.

# Available functions

`llr(k)` - Accepts a list of `Counter` objects and computes an overall
LLR score, taking each element of the list as one condition and the
key for the counts as the other condition.

`llr_compare(k1, k2)` - Compares the two `Counter` object, entry by
entry, by doing a 2x2 test on each key in either `k1` or `k2`. The
result is a dictionary with the same keys and values computed using
`llr_root`. The results for a particular key will be positive if that key
is more common in `k1` and negative if the key is more common in
`k2`. As an example, we can find words that are interestingly more
common in Hamlet than in the Declaration of Independence using this
function. The file `example-01.py` has a complete program to do
this. The beginning is just reading files and counting the words:

    def count(file):
        with open(file) as f:
            return Counter(re.findall('\w+', re.sub('[\r\n]', ' ', f.read())))
    
    hamlet = count('data/hamlet')
    declaration = count('data/declaration') 
    
After this, we can compare the frequencies:

    diff = llr.llr_compare(hamlet, declaration)

At this point, printing out the words most common in the declaration
is a matter of sorting:

    print("\nMore in Declaration of Independence")
    for k,v in sorted(diff.items(), key=lambda x: x[1])[:10]:
        print(k, v)
    

`llr_2x2(k11, k12, k21, k22)` - Compares two binary conditions to see
if there is an apparent connection. The idea is that we have made a
number of observations that exhibit condition A or B. The number of
times we have seen A and B is k11. The number of times we have seen A
but not B is k12, not A but B is k21 and not A and not B is
k22. Commonly, these are arranged in a so-called contingency table:

|               | A    | not A |
| ------------- | ---- | ----- | 
| **B**         | k11  | k12   |
| **not** **B** | k21  | k22   |

The idea is that `llr_2x2` will give a large score if it appears that
there is a correlation or anti-correlation between A and B. We don't
get any idea whether A and B occurs more than we expect or not, however.

`llr_root(k11, k12, k21, k22)` - Computes a signed value much like
`llr_2x2` that has an added sign that tells us about whether the `k11`
cell is larger or smaller than we might expect if A and B are
independent.

The actual value returned by `llr_root` is the square root of the
value returned by `llr_2x2`. The reason for this is that in the
absence of any correlation between the two conditions, the
the output `llr_2x2` will be chi-squared distributed. That
distribution is the same as the distribution of the square of a
normally distributed value. Since the chi-squared distribution cannot
have a negative value, but the normal distribution can, it makes sense
to take the square root at the same time as we add the sign.

Another nice benefit of taking the square root is that it allows us to
interpret the output of `llr_root` as some number of standard deviations.

# How to test the code

You will need to install `pytest` to run the tests embedded in the
code. It goes like this:

    $ sudo pip install pytest
      ... stuff ...
    $ py.test tests.py -v
    ============================= test session starts =============================
    platform darwin -- Python 2.7.10, pytest-2.9.2, py-1.4.31, pluggy-0.3.1 -- /usr/bin/python
    cachedir: .cache
    rootdir: /Users/tdunning/Apache/python-llr, inifile: 
    collected 6 items 
    
    tests.py::test_llr PASSED
    tests.py::test_compare PASSED
    tests.py::test_root PASSED
    tests.py::test_rowSums PASSED
    tests.py::test_colSums PASSED
    tests.py::test_entropy PASSED
    
    ========================== 6 passed in 0.04 seconds ===========================

You can also install the pytest coverage tool to find out that the
tests are comprehensive in terms of lines of code:

    $ sudo pip install pytest-cov
    $ py.test --cov=llr tests.py
    ======================================= test session starts ========================================
    platform darwin -- Python 2.7.10, pytest-2.9.2, py-1.4.31, pluggy-0.3.1
    rootdir: /Users/tdunning/Apache/python-llr, inifile:
    plugins: cov-2.3.0
    collected 6 items

    tests.py ......

    ---------- coverage: platform darwin, python 2.7.10-final-0 ----------
    Name     Stmts   Miss  Cover
    ----------------------------
    llr.py      37      0   100%


    ===================================== 6 passed in 0.02 seconds =====================================
