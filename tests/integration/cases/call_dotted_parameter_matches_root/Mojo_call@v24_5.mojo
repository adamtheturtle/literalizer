@fieldwise_init
struct _OuterType(Copyable, Movable):
    def inner(self, outer: Int, n: Int):
        pass
def main():
    var outer = _OuterType()
    outer.inner(1, 2)
