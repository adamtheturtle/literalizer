@fieldwise_init
struct _FooType(Copyable, Movable):
    def bar(self, var x: List[Int]):
        pass
@fieldwise_init
struct _FooType(Copyable, Movable):
    var Foo: _FooType
@fieldwise_init
struct _AType(Copyable, Movable):
    var foo: _FooType
def main():
    var a = _AType(_FooType(_FooType()))
    a.foo.Foo.bar(List([1]))
