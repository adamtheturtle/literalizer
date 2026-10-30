using System;
class Check {
class FooType_2 { public object? bar(object? x = null) => null; }
class FooType_1 { public FooType_2 Foo = new FooType_2(); }
class AType_ { public FooType_1 foo = new FooType_1(); }
static AType_ a = new AType_();
    public static void Main() {
var my_data = a.foo.Foo.bar(ValueTuple.Create(1));
    _ = my_data;
    }
}
