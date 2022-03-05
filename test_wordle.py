from ast import Assert
from cmath import exp
from webbrowser import get
import pytest
from wordle_start import word2perm, Wordle

word_testdata = [
  ('', [], []),
  ('a', ['a'], ['a']),
  ('abcd', ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd']),
  ('aaa', ['a'], ['a', 'a', 'a']),
  ('abcba', ['a', 'b', 'c'], ['a', 'a', 'b', 'b', 'c']),
]
@pytest.mark.parametrize("word,letters,anagram", word_testdata)
def test_get_letters(word, letters, anagram):
  actual = word2perm(word)
  assert str(actual) == str(letters)

overlap_testdata = [
  ('proud', 'misty', 0),
  ('proud', 'pride', 3),
  ('moody', 'body', 3),
  ('meats', 'steam', 5),
  ('meats', 'amaze', 3)
]

@pytest.mark.parametrize('word1,word2,expected', overlap_testdata)
def test_overlap_count(word1, word2, expected):
  p1 = word2perm(word1)
  p2 = word2perm(word2)
  overlap1 = p1.overlap_count(p2)
  overlap2 = p2.overlap_count(p1)
  assert overlap1 == overlap2
  assert overlap1 == expected

perm_testdata = [
  ('word',
    {word2perm('dorw'): {'word'} }
  ),
   ('woorddr',
    {word2perm('dorw'): {'woorddr'} }
  )
]
@pytest.mark.parametrize("word,_covered", perm_testdata)
def test_process_word(word, _covered):
  a = Wordle()
  a.process_word(word)
  assert a.perm2words == _covered

def test_ingest_word():
  a = Wordle()
  a.ingest_words(['steam', 'meats', 'amaze', 'blaze', 'steem'])
  assert a.perm2words[word2perm('meats')] == {'steam', 'meats'}
  assert a.perm2words[word2perm('amaze')] == {'amaze'}
  assert a.perm2words[word2perm('blaze')] == {'blaze'}
  assert a.perm2words[word2perm('steem')] ==  {'steem'}

def test_find_maxperms():
  a = Wordle()
  a.ingest_words(['steam', 'meats', 'amaze', 'blaze', 'steem'])
  maxperms = a.find_maxperms()
  assert set(maxperms) == set(map(word2perm, ['steam', 'blaze']))

def test_compute_perm_weights():
  a = Wordle()
  #a.ingest_words(['steam', 'meats', 'amaze', 'blaze', 'steem'])
  maxperms = list(map(word2perm, ['steam', 'blaze', 'sound', 'beach', 'pound']))
  permweights = a.compute_perm_weights(maxperms)
  """
           steam    blaze    sound    beach   pound
    steam x            2       1        2       0
    blaze   2          x       0        3       0
    sound   1          0       x        0       4
    beach   2          3       0        x       0
    pound   0          0       4        0       x
    ==================================================
           5           5       5        5       4
  """
  assert permweights[word2perm('steam')] == 5
  assert permweights[word2perm('blaze')] == 5
  assert permweights[word2perm('sound')] == 5
  assert permweights[word2perm('beach')] == 5
  assert permweights[word2perm('pound')] == 4

