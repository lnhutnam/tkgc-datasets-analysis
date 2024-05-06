# Rút trích mẫu quan hệ đồng hiện
from collections import defaultdict


def check_symmetry(
    relation: str, relation_2_facts: defaultdict, tolerance: float = 0.5
):
    """Function for checking relaiton symmetric patterns

    Parameters
    ----------
    relation
        input relation
    relation_2_facts
        _description_
    tolerance, optional
        _description_, by default 0.5

    Returns
    -------
        _description_
    """
    print(f"Checking symmetric for relation: {relation}")

    numerator_count = 0
    denominator_count = 0

    facts_with_that_relation = relation_2_facts[relation]
    for x, r, y, t in facts_with_that_relation:
        if x == y:
            continue
        denominator_count += 1
        if (y, r, x, t) in facts_with_that_relation:
            numerator_count += 1

    if numerator_count == 0:
        return str("antisymmetry")

    if (float(numerator_count) / float(denominator_count)) >= tolerance:
        return str("symmetry")
    else:
        return None


def check_reflexivity(
    relation: str, relation_2_facts: defaultdict, tolerance: float = 0.5
):
    """_summary_

    Parameters
    ----------
    relation
        _description_
    relation_2_facts
        _description_
    tolerance, optional
        _description_, by default 0.5

    Returns
    -------
        _description_
    """
    facts_with_that_relation = relation_2_facts[relation]

    heads = set()
    for fact in facts_with_that_relation:
        heads.add((fact[0], fact[3]))

    reflexive_count = 0
    overall_count = 0
    for head, tau in heads:
        overall_count += 1
        if (head, relation, head, tau) in facts_with_that_relation:
            reflexive_count += 1

    if reflexive_count == 0:
        return str("irreflexive")
    if (float(reflexive_count) / float(overall_count)) >= tolerance:
        return str("reflexive")
    else:
        return None


def check_transitivity(
    relation: str,
    relation_2_train_facts: defaultdict,
    head_2_facts: str,
    tolerance: float = 0.5,
):
    facts_with_that_relation = relation_2_train_facts[relation]

    all_chains_count = 0
    transitive_chains_count = 0

    for step_one_fact in facts_with_that_relation:
        (head1, relation1, tail1, tau1) = step_one_fact

        if head1 == tail1:
            continue

        for step_two_fact in head_2_facts[tail1]:
            (head2, relation2, tail2, tau2) = step_two_fact

            if tau1 != tau2:
                continue
            if relation2 != relation:
                continue
            if head2 == tail2 or tail2 == head1:
                continue

            all_chains_count += 1

            if (head1, relation, tail2, tau1) in facts_with_that_relation:
                transitive_chains_count += 1
    if (
        transitive_chains_count > 0
        and (float(transitive_chains_count) / float(all_chains_count)) >= tolerance
    ):
        return str("transitivity")
    else:
        return None


def check_inverse(
    relation1: str,
    relation2: str,
    relation_2_facts: defaultdict,
    tolerance: float = 0.5,
):
    facts_with_that_relation1 = relation_2_facts[relation1]
    facts_with_that_relation2 = relation_2_facts[relation2]

    numerator_count = 0
    denominator_count = 0

    for x, _, y, t in facts_with_that_relation1:
        if (y, relation2, y, t) in facts_with_that_relation2:
            numerator_count += 1
        else:
            denominator_count += 1
            
    if numerator_count == 0:
        return None

    if (float(numerator_count) / float(denominator_count)) >= tolerance:
        return str("inverse"), relation2
    else:
        return None
    
