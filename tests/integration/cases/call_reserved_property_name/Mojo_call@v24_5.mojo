@fieldwise_init
struct _FooType(Copyable, Movable):
    def class(self, value: Int):
        pass
def main():
    var foo = _FooType()
    foo.class(1)
