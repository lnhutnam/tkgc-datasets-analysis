from collections import defaultdict


def checking_aggregation(ent, graph):
    ent_lst = set()
    rel_lst = set()
    ts_lst = set()
    head_2_facts = defaultdict(lambda: set())
    tail_2_facts = defaultdict(lambda: set())
    rel_2_facts = defaultdict(lambda: set())
    ts_2_facts = defaultdict(lambda: set())

    results = set()

    for s, r, o, t in graph.test_quadruples:
        ent_lst.add(s)
        ent_lst.add(o)
        rel_lst.add(r)
        ts_lst.add(t)
        head_2_facts[s].add((s, r, o, t))
        tail_2_facts[o].add((s, r, o, t))
        rel_2_facts[r].add((s, r, o, t))
        ts_2_facts[t].add((s, r, o, t))

    for t in ts_lst:
        for r in rel_lst:
            for e in ent_lst:
                if e != ent:
                    if (ent, r, e, t) in graph.test_quadruples or (
                        e,
                        r,
                        ent,
                        t,
                    ) in graph.test_quadruples:
                        results.add(head_2_facts[ent])
                        results.add(tail_2_facts[ent])

    return results
