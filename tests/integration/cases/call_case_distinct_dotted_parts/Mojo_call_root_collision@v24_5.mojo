@fieldwise_init
struct _FooType1(Copyable, Movable):
    def bar(self, var x: List[Int]):
        pass
@fieldwise_init
struct _FooType0(Copyable, Movable):
    var Foo: _FooType1
def main():
    var foo = _FooType0(_FooType1())
    foo.Foo.bar(List([1]))
