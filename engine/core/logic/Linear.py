class Linear:

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, b):
        self.root      = b.get('primitives')
        self.position  = 0
        self.completed = False

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def mutate(self):
        if self.position >= len(self.root):
            self.completed = True
            self.position  = 0
            return
        if self.root[self.position].get('ignore'): # TODO: IS THIS STILL OK?
            self.position += 1
            return
        if not self.root[self.position].completed:
           self.root[self.position].mutate()
        else:
            self.position += 1

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        data = []
        for item in self.root:
            r = item.render()
            if type(r).__name__ == "generator": r = r.next()
            data.append("".join(r))
        return data

