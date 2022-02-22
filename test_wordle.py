from ast import Assert
from cmath import exp
from webbrowser import get
import pytest
from wordle_crack import get_letters, get_anagram, Anagram

word_testdata = [
  ('', [], []),
  ('a', ['a'], ['a']),
  ('abcd', ['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd']),
  ('aaa', ['a'], ['a', 'a', 'a']),
  ('abcba', ['a', 'b', 'c'], ['a', 'a', 'b', 'b', 'c']),
]
@pytest.mark.parametrize("word,letters,anagram", word_testdata)
def test_get_letters(word, letters, anagram):
  actual = get_letters(word)
  assert str(actual) == str(letters)

@pytest.mark.parametrize("word,letters,anagram", word_testdata)
def test_anagram(word, letters, anagram):
  actual = get_anagram(word)
  assert str(actual) == str(anagram)

anagram_testdata = [
  ('word',
    {str(['d', 'o', 'r', 'w']): {'word'} },
    {str(['d', 'o', 'r', 'w']): {'word'}},
    {str(['d', 'o', 'r', 'w']): {str(['d', 'o', 'r', 'w'])}}
  ),
   ('woorddr',
    {str(['d', 'o', 'r', 'w']): {'woorddr'} },
    {str(['d', 'd', 'o', 'o', 'r', 'r', 'w']): {'woorddr'}},
    {str(['d', 'd', 'o', 'o', 'r', 'r', 'w']): {str(['d', 'o', 'r', 'w'])}}
  )
]
@pytest.mark.parametrize("word,_covered,_anagrams,_anagram_subset", anagram_testdata)
def test_process_word(word, _covered, _anagrams, _anagram_subset):
  a = Anagram()
  a.process_word(word)
  assert a.covered == _covered
  assert a.anagrams == _anagrams
  assert a.anagram_subset == _anagram_subset

anagram_coverage_testdata = [
  ('pound,misty,beach,boost,bost',
   {'pound': {'pound'},
    'misty': {'misty'},
    'beach': {'beach'},
    'boost': {'boost', 'bost'},
    'bost': {'boost', 'bost'}}
  )
]
@pytest.mark.parametrize('words,coverage_map', anagram_coverage_testdata)
def test_anagram_coverage(words, coverage_map):
  a = Anagram()
  word_list = words.split(',')
  for word in word_list:
    a.process_word(word)
  a.compute_anagram_coverage()
  
  expected = { str(get_anagram(w)): coverage_map[w] for w in coverage_map.keys() }
  assert a.anagram_coverage == expected
  