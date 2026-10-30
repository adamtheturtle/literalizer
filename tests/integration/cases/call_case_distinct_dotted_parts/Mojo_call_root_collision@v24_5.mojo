@fieldwise_init
struct _FooType(Copyable, Movable):
    def bar(self, var x: List[Int]):
        pass
@fieldwise_init
struct _FooType(Copyable, Movable):
    var Foo: _FooType
def main():
    var foo = _FooType(_FooType())
    foo.Foo.bar(List([1]))
