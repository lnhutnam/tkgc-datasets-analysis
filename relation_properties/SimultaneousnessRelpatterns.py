from utils.datasets import TKG


def checking_symmetric(rel, rel_2_facts):
    # for all s, r, o, t
    # r(s, o, t) ^ r(o, s, t) holds True
    facts_with_that_rel = rel_2_facts[rel]

    results = set()
    for x, _, y, t in facts_with_that_rel:
        if x == y:
            continue
        if (y, rel, x, t) in facts_with_that_rel:
            results.add((y, rel, x, t))
            results.add((x, rel, y, t))

    return results


# def checking_antisymmetric(rel, rel_2_facts):
#     # for all s, r, o, t
#     # r(s, o, t) ^ r(o, s, t) holds False
#     facts_with_that_rel = rel_2_facts[rel]

#     results = set()
#     for x, _, y, t in facts_with_that_rel:
#         if x == y:
#             continue
#         if (y, rel, x, t) not in facts_with_that_rel:
#             results.add((y, rel, x, t))
#             results.add((x, rel, y, t))

#     return results


def checking_inverse(rel1, rel2, rel_2_facts):
    # for all s, o, t
    # r1(s, o, t) ^ r2(o, s, t)
    results = set()

    facts_with_that_rel1 = rel_2_facts[rel1]
    facts_with_that_rel2 = rel_2_facts[rel2]
    
    for x, _, y, t1 in facts_with_that_rel2:
        if (y, rel1, x, t1) in facts_with_that_rel1:
            if x != y:
                results.add((y, rel1, x, t1))
                results.add((x, rel2, y, t1))
            

    return results


def checking_composition(rel1, rel2, rel3, rel_2_facts):
    # for all x, y, z, t, rel1, rel2, rel3
    # rel1(x, y, t) ^ rel2(y, z, t) => rel3(x, z, t)
    results = set()

    facts_with_that_rel1 = rel_2_facts[rel1]
    facts_with_that_rel2 = rel_2_facts[rel2]
    facts_with_that_rel3 = rel_2_facts[rel3]

    for x, _, y, t in facts_with_that_rel1:
        if x != y:
            for xx, _, yy, tt in facts_with_that_rel2:
                if t == tt and y == xx:
                    if (x, rel3, yy, t) in facts_with_that_rel3:
                        results.add((x, rel1, y, t))
                        results.add((xx, rel2, yy, t))
                        results.add((x, rel3, yy, t))

    return results
