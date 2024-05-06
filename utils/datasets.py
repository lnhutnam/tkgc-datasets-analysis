import os


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
        self.relationships = set()
        self.timestamps = set()

        print("Reading train quadruples for %s..." % self.name)
        self.train_quadruples = self._read_quadruples(self.train_path, separator)
        print("Reading validation quadruples for %s..." % self.name)
        self.valid_quadruples = self._read_quadruples(self.valid_path, separator)
        print("Reading test quadruples for %s..." % self.name)
        self.test_quadruples = self._read_quadruples(self.test_path, separator)

        self.num_entities = len(self.entities)
        self.num_relations = len(self.relationships)
        self.num_timestamps = len(self.timestamps)

    def _read_quadruples(self, quadruples_path, separator="\t"):
        quadruples = []
        with open(quadruples_path, "r") as quadruples_file:
            lines = quadruples_file.readlines()
            for line in lines:
                # line = html.unescape(line)
                head, relationship, tail, tau = line.strip().split(separator)
                quadruples.append((head, relationship, tail, tau))
                self.entities.add(head)
                self.entities.add(tail)
                self.relationships.add(relationship)
                self.timestamps.add(tau)

        return quadruples
