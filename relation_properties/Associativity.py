from collections import defaultdict


def checking_associativity(graph):
    ent_lst = set()
    rel_lst = set()
    ts_lst = set()
    results = set()

    for s, r, o, t in graph.test_quadruples:
        ent_lst.add(s)
        ent_lst.add(o)
        rel_lst.add(r)
        ts_lst.add(t)

    for ts in ts_lst:
        for rel in rel_lst:
            for s in ent_lst:
                for o in ent_lst:
                    if s != o:
                        if (s, rel, o, ts) in graph.test_quadruples:
                            results.add((s, rel, o, ts))

    return results
