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

class MaxSize():
    def __init__(self):
        self.obj = "MAX"
        
    def chain_val(self, chain):
        return chain.length

    def cycle_val(self, cycle): 
        return cycle.length

    def altruist_val(self, altruist):
        return 0
    
class MinThreeCycles():
    def __init__(self):
        self.obj = "MIN"

    def chain_val(self, chain):
        return chain.length == 3

    def cycle_val(self, cycle): 
        return cycle.length == 3

    def altruist_val(self, altruist):
        return 0


class MaxBackarcs():
    def __init__(self):
        self.obj = "MAX"
        
    def chain_val(self, chain):
        return chain.length

    def cycle_val(self, cycle): 
        if cycle.length < 3:
            return 0
        return cycle.find_backarcs()

    def altruist_val(self, altruist):
        return 1
    
class MaxOverallWeight():
    def __init__(self):
        self.obj = "MAX"
        
    def chain_val(self, chain):
        return chain.get_chain_weight()

    def cycle_val(self, cycle): 
        return cycle.get_cycle_weight()

    def altruist_val(self, altruist):
        return 0