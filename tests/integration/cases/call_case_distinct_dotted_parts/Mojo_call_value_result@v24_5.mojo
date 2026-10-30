@fieldwise_init
struct _FooType(Copyable, Movable):
    def bar(self, var x: List[Int]) -> None:
        pass
@fieldwise_init
struct _FooType(Copyable, Movable):
    var Foo: _FooType
@fieldwise_init
struct _AType(Copyable, Movable):
    var foo: _FooType
def main():
    var a = _AType(_FooType(_FooType()))
    var my_data = a.foo.Foo.bar(List([1]))
    _ = my_data
