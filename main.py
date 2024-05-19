import argparse
from collections import defaultdict

from utils.datasets import TKG

from relation_properties.SimultaneousnessRelpatterns import (
    checking_symmetric,
    checking_antisymmetric,
    checking_inverse,
    checking_composition,
)
from relation_properties.CrosstimeRelpatterns import (
    ct_check_inversion,
    ct_check_hierarchy,
    ct_check_intersection,
    ct_check_composition, 
    ct_mutual_exclusion
)

from relation_properties.Aggregation import (
    checking_aggregation,
)

import pandas as pd


def export2file(quadruples, filename: str = "output.txt"):
    with open(filename, "w") as f:
        for s, r, o, t in quadruples:
            f.write(f"{s}\t{r}\t{o}\t{t}\n")
        f.close()
    return True


def mining_ctrel(root: str, name: str,):
    graph = TKG(root, name)
    print(f"Number of entities: {graph.num_entities}")
    print(f"Number of relations: {graph.num_relations}")
    print(f"Number of timestamp: {graph.num_timestamps}")
    print(f"Mining cross time relation patterns... on testing set of {graph.name}")

    ent_lst = graph.entities
    rel_lst = graph.relations
    ts_lst  = graph.timestamps
    
    rel_2_facts = defaultdict(lambda: set())

    for s, r, o, t in graph.test_quadruples:
        rel_2_facts[r].add((s, r, o, t))

    # checking for ct inversion
    ct_invs = []
    for rel1 in graph.relations:
        for rel2 in graph.relations:
            if rel1 != rel2:
                ct_invs += list(ct_check_inversion(rel1, rel2, rel_2_facts, graph))
     
    ct_invs = list(set(ct_invs))           
    export2file(ct_invs, graph.home + "/ct_invs")
    
    
    # checking for ct hierarchy
    ct_hierarchy = []
    for rel1 in graph.relations:
        for rel2 in graph.relations:
            if rel1 != rel2:
                ct_hierarchy += list(ct_check_inversion(rel1, rel2, rel_2_facts, graph))
             
    ct_hierarchy = list(set(ct_hierarchy))   
    export2file(ct_hierarchy, graph.home + "/ct_hierarchy")
    
    
    # checking for intersection
    intersection = []
    for rel1 in graph.relations:
        for rel2 in graph.relations:
            for rel3 in graph.relations:
                if rel1 != rel2 and rel1 != rel3 and rel2 != rel3:
                    intersection += list(ct_check_intersection(rel1, rel2, rel3, rel_2_facts, graph))

    intersection = list(set(intersection))
    export2file(intersection, graph.home + "/ct_intersection")
    
    
    # checking for intersection
    comps = []
    for rel1 in graph.relations:
        for rel2 in graph.relations:
            for rel3 in graph.relations:
                if rel1 != rel2 and rel1 != rel3 and rel2 != rel3:
                    comps += list(ct_check_composition(rel1, rel2, rel3, rel_2_facts, graph))

    comps = list(set(comps))
    export2file(comps, graph.home + "/ct_comps")
    


def mining_simurel(root: str, name: str):
    graph = TKG(root, name)

    print(f"Number of entities: {graph.num_entities}")
    print(f"Number of relations: {graph.num_relations}")
    print(f"Number of timestamp: {graph.num_timestamps}")
    print(
        f"Mining simultaneousness relation patterns... on testing set of {graph.name}"
    )

    rel_2_facts = defaultdict(lambda: set())
    rel_2_types = defaultdict(lambda: [])

    for s, r, o, t in graph.test_quadruples:
        rel_2_facts[r].add((s, r, o, t))

    # checking for symmetry
    syms = []
    for rel in graph.relations:
        syms += list(checking_symmetric(rel, rel_2_facts, graph))

    syms = list(set(syms))
    export2file(syms, graph.home + "/syms")

    # checking for anti-symmetry
    antisyms = []
    for rel in graph.relations:
        antisyms += list(checking_antisymmetric(rel, rel_2_facts, graph))

    antisyms = list(set(antisyms))
    export2file(antisyms, graph.home + "/anti_syms")

    # checking for inversion
    invs = []
    for rel1 in graph.relations:
        for rel2 in graph.relations:
            if rel1 != rel2:
                invs += list(checking_inverse(rel1, rel2, rel_2_facts, graph))

    invs = list(set(invs))
    export2file(invs, graph.home + "/invs")

    # checking for composition
    comps = []
    for rel1 in graph.relations:
        for rel2 in graph.relations:
            for rel3 in graph.relations:
                if rel1 != rel2 and rel1 != rel3 and rel2 != rel3:
                    comps += list(checking_composition(rel1, rel2, rel3, rel_2_facts))

    comps = list(set(comps))
    export2file(comps, graph.home + "/comps")


def mining_aggregation(root: str, name: str):
    graph = TKG(root, name)

    print(f"Number of entities: {graph.num_entities}")
    print(f"Number of relations: {graph.num_relations}")
    print(f"Number of timestamp: {graph.num_timestamps}")
    print(
        f"Mining aggregation patterns... on testing set of {graph.name}"
    )

    aggregation = []
    for ent in graph.entities:
        aggregation += list(checking_aggregation(ent, graph))

    print(len(aggregation))
    
    # print(graph.valid_quadruples)

    
        
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Relation type extraction for Temporal knowledge graphs.",
        usage="learner.py [<args>] [-h | --help]",
    )
    parser.add_argument("--data_root", type=str, default=".")
    parser.add_argument("--dataset", type=str, default="ICEWS05-15")
    args = parser.parse_args()
    print(args)
    
    # graph = TKG(args.data_root, args.dataset)
    
    # relation_2_types = main(args.data_root, args.dataset)
    # for key, value in relation_2_types.items():
    #     print(value)

    # mining_ctrel(args.data_root, args.dataset)
    # mining_simurel(args.data_root, args.dataset)
    mining_aggregation(args.data_root, args.dataset)
