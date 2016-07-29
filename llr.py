from collections import Counter 
import math

def llr(k):
    '''Computes an LLR score for a list of Count objects'''
    all = flatten([kx.values() for kx in k])
    rows = rowSums(k)
    cols = colSums(k)
    return 2 * (denormEntropy(rows) + denormEntropy(cols) - denormEntropy(all))

def llr_compare(k1, k2):
    '''Compute root-LLR values for all the things in k1 and k2'''
    t1 = sum(k1.values())
    t2 = sum(k2.values())
    r = {}
    for x in set(k1.keys()).union(set(k2.keys())):
        k11 = k1[x]
        k21 = k2[x]
        k12 = t1 - k11
        k22 = t2 - k21
        r[x] = llr_root(k11, k12, k21, k22)
    return r

def llr_2x2(k11, k12, k21, k22):
    '''Special case of llr with a 2x2 table'''
    return 2 * (denormEntropy([k11+k12, k21+k22]) +
                denormEntropy([k11+k21, k12+k22]) -
                denormEntropy([k11, k12, k21, k22]))

def llr_root(k11, k12, k21, k22):
    '''Computes a score for a 2x2 contingency table, but then adds a sign according to whether k11 is larger (result is positive) or smaller (result is negative) than might be expected. The magnitude of the result can be roughly interpreted on a scale similar to standard deviations'''
    row = k11 + k21
    total = (k11 + k12 + k21 + k22)
    sign = cmp(float(k11) / (k11 + k12), float(row) / total)
    return math.copysign(math.sqrt(llr_2x2(k11, k12, k21, k22)), sign)

def flatten(list_of_lists):
    '''Iterates through the elements in a list of lists'''
    for xl in list_of_lists:
        for x in xl:
            yield x

def rowSums(k):
    '''Combines a list of counters into a summed counter'''

def colSums(k):
    '''Computes a list of total counts from a list of Count objects'''
    return [sum(x.values()) for x in k]

def denormEntropy(counts):
    '''Computes the entropy of a list of counts scaled by the sum of the counts. If the inputs sum to one, this is just the normal definition of entropy'''
    counts = list(counts)
    total = float(sum(counts))
    # Note tricky way to avoid 0*log(0)
    return -sum([k * math.log(k/total + (k==0)) for k in counts])

