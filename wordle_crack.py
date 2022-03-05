"""Cracking wordle by finding the optimal sequence of first two words.

This program analyzes five letter words to find a collection of two word sets
that probabilistically discover the most number of characters to enable cracking
the word in three or four attempts.
"""


"""Definition:

Word = seq(Char)
Perm = set(Char)
Word2Perm: Word -> Perm
Perm2Word: Perm -> set(Word)
PermIndex: Perm -> Number -> Number
   PermIndex[p][c] gives the number of words whose permutation
   p' is a subset of p and #p' = c

PermCoverage: Perm -> Number
   PermCoverage[p] = Sum PermIndex[p][c] for all c

OverlapCount: Perm x Perm -> Number
   Number of characters common in two permutations

OverlapIndex: Perm -> Number -> set(Perm)
  OverlapIndex[p][c] gives the set of Perms with which p has overlap count of c.

PermWeight: Perm -> Number
  PermWeight[p] = c * len(OverlapIndex(p)[c]) for all c

Strategy:
   Compute perms for all Words
   Keep perms of length 5
   While there is a perm remaining:
      Compute PermWeight of all perms
      Select a perm with the highest PermWeight
      Remove all perms with non-zero OverlapCount with selected perm
   

"""
from collections import defaultdict

from pytest import PytestUnknownMarkWarning

class Perm(object):
  def __init__(self, word):
    self.letters = sorted(list(set(word)))
  def overlap_count(self, __o) -> int:
    return len (set(self.letters) & set(__o.letters))
  def __hash__(self) -> int:
      return hash(str(self))
  def __eq__(self, __o: object) -> bool:
      return str(self.letters) == str(__o.letters)
  def __str__(self):
    return str(self.letters)
  def __repr__(self):
    return str(self.letters)

def word2perm(word):
  return Perm(word)
class WordleDictionary(object):
  def __init__(self):
    # word list 
    self.word_list = []
    # perm2words: Perm -> set(words)
    self.perm2words = defaultdict(lambda: set())

  def process_word(self, word):
    self.word_list.append(word)
    perm = word2perm(word)
    self.perm2words[perm].add(word)

  def filter_maxperms(self):
    self.maxperms = []
    for perm in self.perm2words.keys():
      if len(perm.letters) == 5:
        self.maxperms.append(perm)

  def compute_perm_weights(self, perms_list):
    perm_weights = defaultdict(lambda:0)
    for p1 in perms_list[0:-1]:
      for p2 in perms_list[1:]:
        c = p1.overlap_count(p2)
        perm_weights[p1] += c
        perm_weights[p2] += c
    return perm_weights

  def find_largest_perm_weight(self, perm_weights):
    keyfn = lambda x: perm_weights[x]
    pordered = sorted(perm_weights.keys(), key=keyfn, reverse=True)
    return pordered[0]
  
  def find_wordle_order(self):
    self.filter_maxperms()
    work_list = self.maxperms
    while len(work_list) > 0:
      perm_weights = self.compute_perm_weights(work_list)
      largest_perm = self.find_largest_perm_weight(perm_weights)
      print(largest_perm, perm_weights[largest_perm])
      filterfn = lambda x: x.overlap_count(largest_perm) == 0
      work_list = list(filter(filterfn, work_list))

  def ingest_words(self, word_stream):
    for word in word_stream:
      self.process_word(word)

if __name__ == "__main__":
  wordfile = "wordlist.txt"
  wordle = WordleDictionary()
  with open(wordfile, "r") as fp:
    wordle.ingest_words(map(lambda word: word.strip(), fp.readlines()))
  wordle.find_wordle_order()


