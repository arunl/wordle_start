"""Cracking wordle by finding the optimal sequence of first two words.

This program analyzes five letter words to find a collection of two word sets
that probabilistically discover the most number of characters to enable cracking
the word in three or four attempts.
"""


"""Strategies

Strategy 1:

Given a set of 5 letter words, find a word that covers the most words.
Remove all the words covered from the list of words.
Repeat until there are no words left. 

Strategy 2:

For a given set of words, find a word that has no duplicate letters and covers the most words.
Remove all the words covered from the list of words, remove all the covered letters.
Repeat until until there are no letters or no words left. 

"""

"""Algorithm

- Function:
    letter_count: word -> letter -> count

- Read the list of words and construct the following tables:
  - letter_frequency: letter -> duplicate -> count
      where duplicate is value from 0 to 5
        letter_frequency[c][i] gives the number of words where letter c appears at least i times.

  - covered: seq(letter) -> set(words)
      covered[C] = {W, ..} where
      - C is an ordered sequence of unique letters and
      - W is a word that is made up of only letters in C (possibly repeating)
  - anagrams: seq(letter) -> set(words)  
      anagrams[A] = {W, ..} where
        - A is an ordered sequence of letters, same length as W and
        - W is a word that is an anagram of those letters

  - anagram_subset: seq(letter) -> set(seq(letter))
      anagram_subset[A] = { C, ..} where 
        - A is an index in anagrams
        - C is an index in covered and 
        - C is a subset of A

- Use the above compute the following
  - anagram_coverage: seq(letter) -> set(words)
    anagram_coverage[A] = {W, ..} where
      exists C in anagram_subset[A] and
      W is in covered[C]
  
- Implementing Stategies
  sort anagram_coverage on decreasing order of length of words
  pick anagram A with most words
  selected_anagrams = [A]
  for A' in anagram_coverage.keys():
    if strategy 2:
    -   continue if A' has non-zero intersection with anagram in selected_anagrams
    - put A' in selected_anagrams
  
  selected_anagrams gives the list of words to choose.
  
"""
from collections import defaultdict

class LetterSet(object):
  def __init__(self, word):
    self.letters = sorted(list(set(word)))
  def __str__(self):
    return str(self.letters)

def get_letters(word):
  return LetterSet(word)

class LetterBag(object):
  def __init__(self, word):
    self.letters = sorted(list(word))
  def __str__(self):
    return str(self.letters)

def get_anagram(word):
  return LetterBag(word)

class Anagram(object):
  def __init__(self):
    # covered: LetterSet -> set(words)
    self.covered = defaultdict(lambda: set())
    # anagrams: LetterBag -> set(words)  
    self.anagrams = defaultdict(lambda:set())
    # anagram_subset: LetterBag -> set(LetterSet)
    self.anagram_subset = defaultdict(lambda: set())
    # anagrams_coverage: LetterBag -> set(words)  
    self.anagram_coverage = defaultdict(lambda:set())

  def process_word(self, word):
    letters = get_letters(word)
    anagram = get_anagram(word)
    self.covered[letters].add(word)
    self.anagrams[anagram].add(word)
    self.anagram_subset[anagram].add(letters)

  def compute_anagram_coverage(self):
    for _anagram in self.anagrams.keys():
      for _letters in self.anagram_subset[_anagram]:
        self.anagram_coverage[_anagram].update(self.covered[_letters])
