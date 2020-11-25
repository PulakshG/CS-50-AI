import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    #print("one_gene ",one_gene)
    #print("two_genes ",two_genes)
    #print("have_trait ",have_trait)
    jp = 1.0
    for p in people:
        pg = gene(p,people,one_gene,two_genes)#probability has gene
        #print("pg ",pg)
        t = trait(p,people,one_gene,two_genes,have_trait)#probability has trait given gene situation
        #print("t ",t)
        
        jp *= float(pg*t) 
        #print("jp", jp)
    #print (jp)
    return jp
    #raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    #print("before ",probabilities)
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p
    #print("after ",probabilities)

    #raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    #print(probabilities)
    for person in probabilities:
        p = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2] 

        probabilities[person]["gene"][0] = probabilities[person]["gene"][0]/p
        probabilities[person]["gene"][1] = probabilities[person]["gene"][1]/p
        probabilities[person]["gene"][2] = probabilities[person]["gene"][2]/p
        
        p = probabilities[person]["trait"][False] + probabilities[person]["trait"][True] 

        probabilities[person]["trait"][False] = probabilities[person]["trait"][False]/p
        probabilities[person]["trait"][True] = probabilities[person]["trait"][True]/p

    #raise NotImplementedError


def gene(p,people,one_gene,two_genes):
    if people[p]["mother"] == None:
        if p in one_gene:
            return PROBS["gene"][1]
        elif p in two_genes:
            return PROBS["gene"][2]
        else:
            return PROBS["gene"][0]
    else:
        if p in one_gene:
            return gene_conditions(parents(people, p, one_gene, two_genes),1)
        elif p in two_genes:
            return gene_conditions(parents(people, p, one_gene, two_genes),2)
        else:
            return gene_conditions(parents(people, p, one_gene, two_genes),0)

def trait(p,people,one_gene,two_genes,have_trait):
    k=None
    if p in one_gene:
        k=1
    elif p in two_genes:
        k=2
    else:
        k=0

    if p in have_trait:
        return PROBS["trait"][k][True]
    else:
        return PROBS["trait"][k][False]

def gene_conditions(parent, condition):
    pm1 = prob_parent(1,parent["mother"])
    pm0 = 1-pm1
    pf1 = prob_parent(1,parent["father"])
    pf0 = 1-pf1

    if condition==0:
        return pm0*pf0
    elif condition==1:
        return (pm0*pf1)+(pm1*pf0)
    else:
        return pm1*pf1

def parents(people, p, one_gene, two_genes ):
    parent={}
    ar=["mother","father"]
    for i in range(2):
        if people[p][ar[i]] in one_gene:
            parent[ar[i]]=1
        elif people[p][ar[i]] in two_genes:
            parent[ar[i]]=2
        else:
            parent[ar[i]]=0
    return parent

def prob_parent(passed_genes, carrier_genes):
    if passed_genes==0:
        if carrier_genes==0:
            return (1-PROBS["mutation"])
        elif carrier_genes==1:
            return 0.5
        else:
            return PROBS["mutation"]
    else:
        if carrier_genes==0:
            return PROBS["mutation"]
        elif carrier_genes==1:
            return 0.5
        else:
            return (1-PROBS["mutation"])

if __name__ == "__main__":
    main()
