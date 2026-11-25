using System;
class Check {
class FoobarType_ { public object? bar(object? x = null) => null; }
class Foo_BarType_ { public FoobarType_ fooBar = new FoobarType_(); }
class AType_ { public Foo_BarType_ foo_bar = new Foo_BarType_(); }
static AType_ a = new AType_();
    public static void Main() {
a.foo_bar.fooBar.bar(ValueTuple.Create(1));
    }
}
