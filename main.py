import argparse
from collections import defaultdict

from utils.datasets import TKG

from relation_properties.simultaneousness_relpatterns import (
    check_symmetry,
    check_reflexivity,
    check_transitivity,
)


def main(root: str, name: str):
    dataset = TKG(root, name)
    print(dataset.num_entities)
    print("Computing the mappings <relation name -> type> in %s training set..." % name)

    relation_2_types = defaultdict(lambda: [])

    relation_2_facts = defaultdict(lambda: set())
    head_2_facts = defaultdict(lambda: set())

    for head, relation, tail, tau in dataset.test_quadruples:
        relation_2_facts[relation].add((head, relation, tail, tau))
        head_2_facts[head].add((head, relation, tail, tau))

    for relation in dataset.relationships:
        relation_2_types[relation] = []

        # is_reflexive = check_reflexivity(relation, relation_2_facts)
        # is_symmetric = check_symmetry(relation, relation_2_facts)
        is_transitive = check_transitivity(relation, relation_2_facts, head_2_facts)

        # if is_reflexive is not None:
        #     relation_2_types[relation].append(is_reflexive)

        # if is_symmetric is not None:
        #     relation_2_types[relation].append(is_symmetric)

        if is_transitive is not None:
            relation_2_types[relation].append(is_transitive)

    return relation_2_types


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Relation type extraction for Temporal knowledge graphs.",
        usage="learner.py [<args>] [-h | --help]",
    )
    parser.add_argument("--data_root", type=str, default=".")
    parser.add_argument("--dataset", type=str, default="GDELT")
    args = parser.parse_args()
    print(args)
    relation_2_types = main(args.data_root, args.dataset)
    for key, value in relation_2_types.items():
        print(value)