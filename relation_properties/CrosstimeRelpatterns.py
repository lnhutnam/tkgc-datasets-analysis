# Rút trích mẫu quan hệ liên thời gian
from utils.datasets import TKG


# Inversion
def ct_check_inversion(rel1, rel2, rel_2_facts, graph):
    # r_1(x, y | tau_1) <=> r_2(y, x | tau_2)
    results = set()

    ts_lst = graph.timestamps
    quads = graph.test_quadruples

    facts_with_that_rel1 = rel_2_facts[rel1]
    facts_with_that_rel2 = rel_2_facts[rel2]

    for x, _, y, t1 in facts_with_that_rel2:
        for ts in ts_lst:
            if ts != t1:
                if (y, rel1, x, ts) in facts_with_that_rel1:
                    if x != y:
                        if (x, rel1, y, t1) in quads and (y, rel2, x, ts) in quads:
                            results.add((x, rel1, y, t1))
                            results.add((y, rel2, x, ts))
    return results


# Hierarchy
def ct_check_hierarchy(rel1, rel2, rel_2_facts, graph):
    # r_1(x, y | tau_1) => r_2(x, y | tau_2)

    results = set()

    ts_lst = graph.timestamps
    quads = graph.test_quadruples

    facts_with_that_rel1 = rel_2_facts[rel1]
    facts_with_that_rel2 = rel_2_facts[rel2]

    for x, _, y, t1 in facts_with_that_rel2:
        for ts in ts_lst:
            if ts != t1:
                if (x, rel1, y, ts) in facts_with_that_rel1:
                    if x != y:
                        if (x, rel1, y, t1) in quads and (x, rel2, y, ts) in quads:
                            results.add((x, rel1, y, t1))
                            results.add((x, rel2, y, ts))

    return results


# Intersection
def ct_check_intersection(rel1, rel2, rel3, rel_2_facts, graph):
    # r_1(x, y | tau_1) ^ r_2(x, y | tau_2) => r_3(x, y | tau_3)
    results = set()

    ts_lst = graph.timestamps
    quads = graph.test_quadruples

    facts_with_that_rel1 = rel_2_facts[rel1]
    facts_with_that_rel2 = rel_2_facts[rel2]
    facts_with_that_rel3 = rel_2_facts[rel3]

    for x, _, y, t in facts_with_that_rel1:
        for xx, _, yy, tt in facts_with_that_rel2:
            if x == xx and y == yy and t != tt:
                for ts in ts_lst:
                    if ts != t and ts != tt:
                        if (x, rel3, y, ts) in facts_with_that_rel3 and (x, rel3, y, ts) in quads:
                            results.add((x, rel3, y, ts))

    return results


# Composition
def ct_check_composition(rel1, rel2, rel3, rel_2_facts, graph):
    # r_1(x, y | tau_1) ^ r_2(y, z | tau_2) => r_3(x, z | tau_3)
    results = set()

    ts_lst = graph.timestamps
    quads = graph.test_quadruples

    facts_with_that_rel1 = rel_2_facts[rel1]
    facts_with_that_rel2 = rel_2_facts[rel2]
    facts_with_that_rel3 = rel_2_facts[rel3]

    for x, _, y, t in facts_with_that_rel1:
        for yy, _, z, tt in facts_with_that_rel2:
            if y == yy and t != tt:
                for ts in ts_lst:
                    if ts != t and ts != tt:
                        if (x, rel3, z, ts) in facts_with_that_rel3 and (
                            x,
                            rel3,
                            z,
                            ts,
                        ) in quads:
                            results.add((x, rel3, z, ts))

    return results


# Mutual
def ct_mutual_exclusion():
    # r_1(x, y | tau_1) ^ r_2(x, y | tau_2) =>
    pass
