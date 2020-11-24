import Base
import Clusters
import random
__author__ = 'Aster'


def letterfreqs(lets):
    """
    :param lets: a list of tuples (letter, frequency)
    :return: a list of each letter frequency times
    """
    lfreqs = []
    for (i, j) in lets:
        c = 0
        while c < j:
            lfreqs.append(i)
            c += 1
    return lfreqs


def rep(l, let, rp='.'):
    """
    :param l: a list of one-letter strings
    :param let: a one-letter string
    :param rp: what to replace let with
    :return: first instance of let replaced with rp
    """
    l[l.index(let)] = rp


def allophones(string):
    """
    :param string: a string
    :return: the string calibrated for allophones in the language
    """
    working = list(string)
    if working[-1] == 'ð':
        working[-1] = 'θ'
    while 'z' in working:
        rep(working, 'z', 'ts')
    while 't' in working:
        try:
            if working[working.index('t') + 1] == 'j':
                rep(working, 't', 'tʃ')
            else:
                rep(working, 't')
        except:
            rep(working, 't')
    while '.' in working:
        rep(working, '.', 't')
    while 't' in working:
        try:
            if working[working.index('t') - 1] == 'i':
                rep(working, 't', 'tʃ')
            else:
                rep(working, 't')
        except:
            rep(working, 't')
    while '.' in working:
        rep(working, '.', 't')
    while 't' in working:
        try:
            if working[working.index('t') - 1] == 'y':
                rep(working, 't', 'tʃ')
            else:
                rep(working, 't')
        except:
            rep(working, 't')
    while '.' in working:
        rep(working, '.', 't')
    while 's' in working:
        try:
            if working[working.index('s') + 1] == 'j':
                rep(working, 's', 'ʃ')
            else:
                rep(working, 's')
        except:
            rep(working, 's')
    while '.' in working:
        rep(working, '.', 's')
    done = ''
    for j in working:
        done += j
    return done


def clustcheck(string, lnth):
    """
    :param string: a string
    :param lnth: length of final name
    :return: checks for legality of continuing consonant or vowel clusters
    """
    conscount = 0
    vowlcount = 0
    poslets = {}
    if string == "":
        poslets = Base.phons.copy()
        poslets = list(poslets.items())
        return letterfreqs(poslets)
    for i in string:
        if i in Base.cons:
            conscount += 1
            vowlcount = 0
        else:
            conscount = 0
            vowlcount += 1
    if conscount == 0:
        poslets = Base.cons.copy()
        poslets = list(poslets.items())
        vlfreq = Base.vowls.copy()
        vlfreq = list(vlfreq.items())
        if vowlcount == 1:
            for (i, j) in vlfreq:
                vlfreq[vlfreq.index((i, j))] = (i, j/20)
            poslets += vlfreq
    elif vowlcount == 0:
        prvclust = string[len(string)-conscount:]
        if conscount == len(string):
            if conscount == 1:
                for i in Clusters.ini.copy():
                    if len(prvclust) < len(i) and prvclust in i:
                        poslets[i[len(prvclust)]] = Base.phons[i[len(prvclust)]]
            # elif conscount == 2:
            #     for i in Clusters.ini.copy():
            #         if len(prvclust) < len(i) and prvclust in i:
            #             poslets[i[len(prvclust)]] = Base.phons[i[len(prvclust)]]/4
            # else:
            #     poslets = Base.vowls.copy()
        # elif conscount == 1 and lnth - 1 == len(string):
            # for i in Base.finl.copy():
            #     if len(prvclust) < len(i) and prvclust in i:
            #         poslets[i[len(prvclust)]] = Base.phons[i[len(prvclust)]]
            # poslets += Base.vowls.copy()
        elif lnth - len(string) >= 2 and conscount == 1:
            # if prvclust[:2] in Clusters.finl:
            #     for i in Clusters.invo.copy():
            #         if prvclust in i[:len(prvclust)]:
            #             poslets[i[len(string)]] = Base.phons[i[len(string)]]
            poslets = Base.cons.copy()
        poslets = list(poslets.items())
        vls = Base.vowls.copy()
        vls = list(vls.items())
        poslets += vls
    poslets = dict(poslets)
    poslets = list(poslets.items())
    return letterfreqs(poslets)


def words(lnth=random.randrange(2, 8), pos=""):
    """
    :param lnth: length of word
    :param pos: part of speech
    :return: a word
    """
    n = ""
    if pos == "":
        pos = input('Enter (n) for noun, anything else for anything else.')
    while len(n) < lnth:
        poslets = clustcheck(n, lnth)
        n += poslets[random.randrange(0, len(poslets))][0]
    if pos == 'n':
        declen = input('Masculine (m), feminine (f), or neuter (n)?')
        n = noun(n, declen)
    # elif pos == 'v':
    #     conj = int(input('Conjugation 1 or 2? Choose 3 for random.'))
    #     n = verb(n, conj)
    # elif pos == 'a':
    #     n += 'zæ'
    n = allophones(n)
    return n


def verb(root, conj):
    """
    :param root: a verb root
    :param conj: which conjugation
    :return: a verb finished in the infinitive
    """
    if conj == 3:
        conj = random.randrange(1, 3)
    if conj == 1:
        root += 'viç'  # CHANGE
    elif conj == 2:
        root += 'soz'  # CHANGE
    return root


def noun(root, declen):
    """
    :param root: a noun root
    :param declen: which declension
    :return: noun finished in nominative case
    """
    try:
        if declen == 'm' or declen == 1:
            if root[-1] not in list(Base.cons.keys()):
                root += 'l'
            root += 'o'
        elif declen == 'f' or declen == 2:
            if root[-1] not in list(Base.cons.keys()):
                root += 'β'
        elif declen == 'n' or declen == 3:
            root += 'ɔð'
        else:
            root = noun(root, random.randrange(0, 3))
    except:
        root = noun(root, random.randrange(0, 3))
    return root

# c=0
# for i in range(1, 100):
#     w = words()
#     if 'j' in z:
#         c+=1
# print(c)

# w = words(2, x)
# print(w)

# NOTE! z here represents affricate ts for ease of coding clusters

# pikuoph