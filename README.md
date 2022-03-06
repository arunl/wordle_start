# wordle_start
To determine two words to start wordle such that they would discover the most number of characters of the
word of the day, and increase the odds of guessing the word in 3 to 4 tries.

## Key idea

Most strategies on cracking wordle that I have come across focus on picking the start word, and they choose 
this first word based on the distribution of letters in a dictionary of words. Some also focus on choosing 
the word so as to discover the most vowels. 

The strategy leads to the obvious question: What do you do after the first word? At that point many focus on
selecting the next word based on the letters found in the first word. This is not a simple exercise though. 
Suppose the first word uncovers one or two letters, that is rules out 3 or 4 letters, then you are not in a
significantly better position since you can make a lot of words with any subset of 22 or 23 letters of the English
alphabet. It is worse if the first word doesn't find any letter? Why, since then you are left with nothing to work with.

I am using a different strategy. I want to uncover the most letters possible in the first two words. In essence, I am 
assuming that the chances that any start word will reduce the space of correct words is very low, so why not select the
first two words with the goal of increasing the odds of guessing the word in 3 or 4 tries and, more so, significantly 
reduce the odds of not being able to guess the word at all. 

To achieve the goal described above, I have restated my objective as follows:  Find two words such that the remaining letters 
make the fewest number of words. It would be ideal if the remaining letters cannot make any word by themselves.

To get the best results the two words should have 10 distinct letters, that is, each word cannot have any repeating character and the two
words cannot share any character. Furthermore, the remaining 16 letters should form as few, preferably, zero words. 

## Algorithm

Here is an outline of the algorithm:

```
Definitions:
  Word = seq(Char)
    A word is a sequence of characters
  Perm = set(Char)   # Permutation
    A permutation is a set of characters, so it cannot have any repeating character
  Word2Perm: Word -> Perm
    A function that creates a permutation of characters from a word.
  Perm2Word: Perm -> set(Word)
    A map that gives the set of words for a permutation
  OverlapCount: Perm x Perm -> Number
    Number of characters common in two permutations
  PermWeight: Perm -> Number
    PermWeight[pi] = Sum(OverlapCount(pi,pj) * len(Perm2Word(pj)), for all pj in Perm)
    
    The weight of a permutation is the sum of the overlap it has with all the words in the dictionary.

Strategy:
   Input a dictionary of words (preferably five letters long)
   Compute perms for all the words
   Keep perms of length 5
   While there is a perm remaining:
      Compute PermWeight of the remaining perms
      Select a perm with the highest PermWeight
      Remove all perms with non-zero OverlapCount with the selected perm
 ```
 
 The order in which the perms are selected in the while loop gives the order of the words. The loop terminates when
 it cannot find any more perms. With the list of words included in the project, the loop terminates after two iterations,
 implying that the remaining letters do not make a word that contains five distinct letters.
 
 ## Result
 So what are the two words selected. Try out the program to find for yourself. If you are not the programming kind, send me a note.
 
 
