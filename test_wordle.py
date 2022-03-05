from ast import Assert
from cmath import exp
from webbrowser import get
import pytest
from wordle_crack import word2perm, WordleDictionary

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
  a = WordleDictionary()
  a.process_word(word)
  assert a.perm2words == _covered

  