import argparse
from collections import defaultdict

from utils.datasets import TKG

from relation_properties.SimultaneousnessRelpatterns import (
    checking_symmetric,
    # checking_antisymmetric,
    checking_inverse,
    checking_composition,
)
from relation_properties.CrosstimeRelpatterns import (
    ct_check_inversion,
    ct_check_hierarchy,
    ct_check_intersion,
    ct_check_composition, 
    ct_mutual_exclusion
)

import pandas as pd


def export2file(quadruples, filename: str = "output.txt"):
    with open(filename, "w") as f:
        for s, r, o, t in quadruples:
            f.write(f"{s}\t{r}\t{o}\t{t}\n")
        f.close()
    return True


def mining_ctrel(root: str, name: str):
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
                
    export2file(ct_invs, "ct_invs")
    
    
    # checking for ct inversion
    ct_hierarchy = []
    for rel1 in graph.relations:
        for rel2 in graph.relations:
            if rel1 != rel2:
                ct_hierarchy += list(ct_check_inversion(rel1, rel2, rel_2_facts, graph))
                
    export2file(ct_hierarchy, "ct_hierarchy")
    


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
    # syms = []
    # for rel in graph.relations:
    #     syms += list(checking_symmetric(rel, rel_2_facts))

    # export2file(syms, "syms")

    # # checking for anti-symmetry
    # syms = []
    # for rel in graph.relations:
    #     syms += list(checking_antisymmetric(rel, rel_2_facts))

    # export2file(syms, "anti_syms")

    # checking for inversion
    invs = []
    for rel1 in graph.relations:
        for rel2 in graph.relations:
            if rel1 != rel2:
                invs += list(checking_inverse(rel1, rel2, rel_2_facts))

    export2file(invs, "invs")

    # checking for composition
    # comps = []
    # for rel1 in graph.relations:
    #     for rel2 in graph.relations:
    #         for rel3 in graph.relations:
    #             if rel1 != rel2 and rel1 != rel3 and rel2 != rel3:
    #                 comps += list(checking_composition(rel1, rel2, rel3, rel_2_facts))

    # export2file(comps, "comps")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Relation type extraction for Temporal knowledge graphs.",
        usage="learner.py [<args>] [-h | --help]",
    )
    parser.add_argument("--data_root", type=str, default=".")
    parser.add_argument("--dataset", type=str, default="ICEWS05-15")
    args = parser.parse_args()
    print(args)
    # relation_2_types = main(args.data_root, args.dataset)
    # for key, value in relation_2_types.items():
    #     print(value)

    mining_ctrel(args.data_root, args.dataset)
    # mining_simurel(args.data_root, args.dataset)
