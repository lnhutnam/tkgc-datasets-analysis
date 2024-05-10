import os
from collections import defaultdict
from datetime import datetime


class TKG:

    def __init__(self, root, name, separator="\t"):

        self.name = name

        self.home = os.path.join(root, "datasets", self.name)
        if not os.path.isdir(self.home):
            raise Exception("Folder %s does not exist" % self.home)

        self.train_path = os.path.join(self.home, "train")
        self.valid_path = os.path.join(self.home, "valid")
        self.test_path = os.path.join(self.home, "test")

        self.entities = set()
        self.relations = set()
        self.timestamps = set()

        if name == "YAGO15k":
            print("Reading train quadruples for %s..." % self.name)
            self.train_quadruples = self._read_quadruples_yago(self.train_path, separator)
            print("Reading validation quadruples for %s..." % self.name)
            self.valid_quadruples = self._read_quadruples_yago(self.valid_path, separator)
            print("Reading test quadruples for %s..." % self.name)
            self.test_quadruples = self._read_quadruples_yago(self.test_path, separator)
        
        else:
            print("Reading train quadruples for %s..." % self.name)
            self.train_quadruples = self._read_quadruples(self.train_path, separator)
            print("Reading validation quadruples for %s..." % self.name)
            self.valid_quadruples = self._read_quadruples(self.valid_path, separator)
            print("Reading test quadruples for %s..." % self.name)
            self.test_quadruples = self._read_quadruples(self.test_path, separator)

        self.num_entities = len(self.entities)
        self.num_relations = len(self.relations)
        self.num_timestamps = len(self.timestamps)
        print(len(self.test_quadruples))

    def _read_quadruples(self, quadruples_path, separator="\t"):
        quadruples = []
        with open(quadruples_path, "r") as quadruples_file:
            lines = quadruples_file.readlines()
            for line in lines:
                head, relation, tail, tau = line.strip().split(separator)
                quadruples.append((head, relation, tail, tau))
                self.entities.add(head)
                self.entities.add(tail)
                self.relations.add(relation)
                self.timestamps.add(tau)

        return quadruples
    
    def _read_quadruples_yago(self, quadruples_path, separator="\t"):
        quadruples = []
        with open(quadruples_path, "r") as quadruples_file:
            lines = quadruples_file.readlines()
            for line in lines:
                fact = line.strip().split(separator)
                if len(fact) == 5:
                    head, relation, tail, _, tau = fact
                    quadruples.append((head, relation, tail, tau))
                    self.entities.add(head)
                    self.entities.add(tail)
                    self.relations.add(relation)
                    self.timestamps.add(tau)
                    
        return quadruples
                    
    def get_stat(
        self,
    ):
        num_entities = self.num_entities
        num_relations = self.num_relations
        num_timestamps = self.num_timestamps
        ts_lst = [datetime.strptime(day, "%Y-%m-%d") for day in self.timestamps]
        min_timestamps = min(ts_lst)
        max_timestamps = max(ts_lst)

        return (
            num_entities,
            num_relations,
            num_timestamps,
            min_timestamps,
            max_timestamps,
        )

    def get_facts_at(self, inp_tau):

        facts = set()
        for head, relation, tail, tau in self.test_quadruples:
            if tau == inp_tau:
                facts.add((head, relation, tail, tau))

        return facts
