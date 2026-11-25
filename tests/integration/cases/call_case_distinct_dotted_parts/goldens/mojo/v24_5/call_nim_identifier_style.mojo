@fieldwise_init
struct _FoobarType(Copyable, Movable):
    def bar(self, var x: List[Int]):
        pass
@fieldwise_init
struct _Foo_barType(Copyable, Movable):
    var fooBar: _FoobarType
@fieldwise_init
struct _AType(Copyable, Movable):
    var foo_bar: _Foo_barType
def main():
    var a = _AType(_Foo_barType(_FoobarType()))
    a.foo_bar.fooBar.bar(List([1]))
