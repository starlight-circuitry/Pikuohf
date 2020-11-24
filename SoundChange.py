import WordGen
import Base
import random

__author__ = 'Aster'

# This is 800 years change, from old common to Pikuof. For the sake of simplicity (and my sanity), let's say, 4-5
# individual changes. Also, these should be sequential, not simultaneous, obviously.

# Also, note that this is a reverse-order list, as they are aged backwards.

# Also, loanwords exist. They can be introduced at any point, remember this. There is a chance for any word that it
# only goes through the last few of these.
# Also, words can be derived from ancient texts and skip a level or two of changes. It could be worth keeping track of
# when words enter the language. See this link:
# https://www.reddit.com/r/conlangs/comments/3gf8mu/a_guide_to_sound_changes/

# List of changes, in chronological order:

# 700 bpd: /ə/ > 0 / VC_#
# 550 bpd: VCC > VCVC
# 300 bpd: /r/ > /l/
# 150 bpd: voiced C > devoiced C / _#


voiced_cons = [('d', 2500), ('β', 5947), ('z', 7056), ('ð', 6131), ('g', 10345), ('l', 13137)]

voiceless_cons = [('t', 2951), ('ɸ', 4309), ('x', 8544), ('k', 9385), ('ɬ', 12765), ('p', 13893)]


def historicalWord(word="", gen=""):
    if word == "":
        word = WordGen.words(pos="x")
        print(word)
    change_chance = 0
    change_threshold = 30

    # define new word as a copy of word
    new_word = ""
    for i in range(len(word)):
        new_word = new_word + word[i]

    # loop 1: chance of devoiced non-nasal C > voiced / _#
    i = len(word)-1
    if word[i] in voiceless_cons:
        change_chance = random.randrange(0, 100)
        if change_chance < change_threshold:
            if word[i] == 't':
                new_word = word[:i] + 'd'
            if word[i] == 'ɸ':
                new_word = word[:i] + 'β'
            if word[i] == 'x':
                new_word = word[:i] + 'γ'
            if word[i] == 'k':
                new_word = word[:i] + 'g'
            if word[i] == 'ɬ':
                new_word = word[:i] + 'l'
            if word[i] == 'p':
                new_word = word[:i] + 'b'

    # update word to reflect this change
    word = ""
    for i in range(len(new_word)):
        word = word + new_word[i]

    # loop 2: chance of /l/ > /r/
    for i in range(len(word)):
        if word[i] == 'l':
            change_chance = random.randrange(0, 100)
            if change_chance < change_threshold:
                new_word = word[:i] + 'r' + word[i+1:]

    # update word to reflect this change
    word = ""
    for i in range(len(new_word)):
        word = word + new_word[i]

    # loop 3: chance of CVC > CC unless #CVC
    change_threshold = 20
    for i in range(1, len(word)-2):
        if word[i] in Base.cons and word[i+1] in Base.vowls and word[i+2] in Base.cons:
            change_chance = random.randrange(0, 100)
            if change_chance < change_threshold:
                new_word = word[:i+1] + word[i+2:]

    # update word to reflect this change
    word = ""
    for i in range(len(new_word)):
        word = word + new_word[i]

    # loop 4: chance of VC_# > VCə
    change_threshold = 30
    if word[-1] in Base.cons:
        change_chance = random.randrange(0, 100)
        if change_chance < change_threshold:
            new_word = word + "ə"

    # update word to reflect this change
    word = ""
    for i in range(len(new_word)):
        word = word + new_word[i]

    return word


def transcribe(string):
    """
    :param string: a string
    :return: the string calibrated for allophones in the language
    """
    working = list(string)
    while 'ɸ' in working:
        WordGen.rep(working, 'ɸ', 'f')
    while 'β' in working:
        WordGen.rep(working, 'β', 'v')
    while 'ð' in working:
        WordGen.rep(working, 'ð', 'th')
    while 'ʔ' in working:
        WordGen.rep(working, 'ʔ', '\'')
    while 'ɲ' in working:
        WordGen.rep(working, 'ɲ', 'ñ')
    while 'ɱ' in working:
        WordGen.rep(working, 'ɱ', 'm')
    while 'ɱ' in working:
        WordGen.rep(working, 'ɱ', 'my')
    while 'ɬ' in working:
        WordGen.rep(working, 'ɬ', 'lh')
    while 'ʌ' in working:
        WordGen.rep(working, 'ʌ', 'u')
    while 'ɔ' in working:
        WordGen.rep(working, 'ɔ', 'au')
    while 'γ' in working:
        WordGen.rep(working, 'γ', 'gh')
    while 'ə' in working:
        WordGen.rep(working, 'ə', 'e')


    return ''.join(working)


print(transcribe(historicalWord()))


for j in range(10):
    s = historicalWord()
    s = transcribe(s)
    s = s + ','
    print(s, end='\n\n')
