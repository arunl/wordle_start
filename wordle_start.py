"""Cracking wordle by finding the optimal sequence of first two words.

This program analyzes five letter words to find two words with
that would discover the most number of characters of the final word. 
This to enable cracking the word in three or four attempts.
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
from math import perm

from pytest import PytestUnknownMarkWarning

class Perm(object):
  """Models an object representing permutations of characters in a word."""
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

class Wordle(object):
  def __init__(self):
    # word list 
    self.word_list = []
    # perm2words: Perm -> set(words)
    self.perm2words = defaultdict(lambda: set())

  def process_word(self, word):
    self.word_list.append(word)
    perm = word2perm(word)
    self.perm2words[perm].add(word)

  def ingest_words(self, word_stream):
    for word in word_stream:
      self.process_word(word)

  def find_maxperms(self):
    maxperms = []
    for perm in self.perm2words.keys():
      if len(perm.letters) == 5:
        maxperms.append(perm)
    return maxperms

  def compute_perm_weights(self, perms_list):
    perm_weights = defaultdict(lambda:0)
    r = range(0, len(perms_list))
    for r1 in r[:-1]:
      p1 = perms_list[r1]
      for r2 in r[r1+1:]:
        p2 = perms_list[r2]
        c = p1.overlap_count(p2)
        perm_weights[p1] += c
        perm_weights[p2] += c
    return perm_weights

  def sort_perms_by_weight(self, perm_weights):
    keyfn = lambda x: perm_weights[x]
    pordered = sorted(perm_weights.keys(), key=keyfn, reverse=True)
    return pordered
  
  def find_wordle_order(self):
    work_list = self.find_maxperms()
    while len(work_list) > 0:
      perm_weights = self.compute_perm_weights(work_list)
      ordered_perms = self.sort_perms_by_weight(perm_weights)
      # print all with highest perms
      largest_perm = ordered_perms[0]
      largest_weight = perm_weights[largest_perm]
      for p in ordered_perms:
        if perm_weights[p] < largest_weight:
          print("next:", perm_weights[p], p, self.perm2words[p])
          break
        print(perm_weights[p], p, self.perm2words[p])
      filterfn = lambda x: x.overlap_count(largest_perm) == 0
      work_list = list(filter(filterfn, work_list))

if __name__ == "__main__":
  wordfile = "wordlist.txt"
  wordle = Wordle()
  with open(wordfile, "r") as fp:
    wordle.ingest_words(map(lambda word: word.strip(), fp.readlines()))
  wordle.find_wordle_order()

  maxperms = wordle.find_maxperms()
