import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.

    if no links:
        for a in page links:
            corpus[a]=1/n
    else:
        for a in page links:
            corpus[a]=((1-d)/n)+(d/number of links)

    """
    pd={}
    n=len(corpus)
    nl=len(corpus[page])
    d=damping_factor
    if nl==0:
        for i in corpus:
            pd[i]=1/n
    else:
        for i in corpus:
            if i in corpus[page]:
                pd[i]=((1-d)/n)+(d/nl)
            else:
                pd[i]=((1-d)/n)
    return pd

    #raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    npd={}
    lis=list(corpus)
    pd = uniform(corpus)
    current=next_node(corpus, pd, lis)
    for i in corpus:
        npd[i]=0.0
    for i in range(n):
        #print("current", current)
        pd=transition_model(corpus, current, damping_factor)
        #print("pd",pd)
        current=next_node(corpus, pd, lis)#transition_model(corpus, current, damping_factor))
        #print("npd[current]",npd[current])
        npd[current]+=1
    #print(npd)
    for i in npd:
        npd[i]=float(npd[i]/n)
    return npd
    #raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pd = uniform(corpus)
    n=len(corpus)
    d=damping_factor
    npd={}
    while True:
        #print("1")
        for current in corpus:
            nl=len(corpus[current])
            prlinks=0.0
            for i in corpus:
                if current in corpus[i]:
                    #print(pd[i])
                    prlinks += float(pd[i]/float(len(corpus[i])))
            npd[current]=((1-d)/n)+(d*prlinks)
            #print("npd[current]",npd[current])
        #print(pd)
        #print(npd)
        if converge(corpus, pd, npd):
            break
        pd=npd.copy()

    return npd
    #raise NotImplementedError
def converge(corpus, pd, npd):
    update=0
    for i in corpus:
        update+=abs(npd[i]-pd[i])
    if update<0.001:
        return True
    else:
        return False
def uniform(corpus):
    pd={}
    n=len(corpus)
    for i in corpus:
        pd[i]=1/n
    return pd

def next_node(corpus,pd,lis):
    weight=[pd[i] for i in lis]
    return random.choices(lis,weight).pop()

if __name__ == "__main__":
    main()
