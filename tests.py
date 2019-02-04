import llr
from collections import Counter 
import math

def test_llr():
    assert llr.llr([Counter('a'), Counter('b')])/math.log(2) == 4
    assert llr.llr([Counter('aa'), Counter('bb')])/math.log(2) == 8
    assert llr.llr([Counter('ab'), Counter('ba')])/math.log(2) == 0
    assert llr.llr([Counter('a'), Counter('ba')]) == 1.0464962875290968

def test_compare():
    actual = llr.llr_compare(Counter('abcabcabcababa'), Counter('cccccc'))
    ref = {'a': 2.3050260628857417, 'c': -3.6024043433364215, 'b': 2.060150982796662}
    assert actual == ref

def test_root():
    assert llr.llr_root(1,0,0,1) == math.sqrt(llr.llr([Counter('a'), Counter('b')]))
    assert llr.llr_root(0,1,1,0) == -math.sqrt(llr.llr([Counter('a'), Counter('b')]))

def test_rowSums():
    s1 = 'abcabcabcababa'
    s2 = 'abcabcdef'
    s3 = 'defghijkabc'
    assert tuple(llr.rowSums([])) == tuple(Counter().values())
    assert tuple(llr.rowSums([Counter(s1)])) == tuple(Counter(s1).values())
    assert tuple(llr.rowSums([Counter(s1), Counter(s2)])) == tuple(Counter(s1 + s2).values())
    assert tuple(llr.rowSums([Counter(s1), Counter(s2), Counter(s3)])) == tuple(Counter(s1 + s2 + s3).values())

def test_colSums():
    x = Counter('abcabcabcababa')
    y = Counter('abcabcdef')
    assert llr.colSums([]) == []
    assert llr.colSums([x]) == [14]
    assert llr.colSums([x,y]) == [14, 9]

def test_entropy():
    assert llr.denormEntropy([0.5,0.5])/math.log(2) == 1
    assert llr.denormEntropy([0.5,0.5,0])/math.log(2) == 1
    assert llr.denormEntropy([0.25,0.25,0.25,0.25])/math.log(2) == 2
    assert llr.denormEntropy([1,1])/math.log(2) == 2
    assert llr.denormEntropy([2,2])/math.log(2) == 4
    assert llr.denormEntropy([2,1,1])/math.log(2) == 6
    assert llr.denormEntropy([1,1,1,1])/math.log(2) == 8
