class path:
    def __init__(self, p, cost):
        self.p = p
        self.cost = cost

    def __lt__(self, other):
        if self.cost > other.cost:
            return True
        else:
            return False

