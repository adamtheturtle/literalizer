@fieldwise_init
struct _FooType(Copyable, Movable):
    def class(self, var value: Int):
        pass
def main():
    var foo = _FooType()
    foo.class(1)
