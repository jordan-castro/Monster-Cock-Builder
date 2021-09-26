class BoxSize(object):
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        super().__init__()

    def box(self, x, y):
        return x, y,self.width, self.height