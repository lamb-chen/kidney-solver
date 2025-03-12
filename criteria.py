class MaxTwoCycles():
    def __init__(self):
        self.obj = "MAX"
        
    def chain_val(self, chain):
        return 1

    def cycle_val(self, cycle):
        if cycle.length == 2: 
            return 1
        return 0

    def altruist_val(self, altruist):
        return 0
    