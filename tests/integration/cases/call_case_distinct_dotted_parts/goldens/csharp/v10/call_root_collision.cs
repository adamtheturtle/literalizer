using System;
class Check {
class FooType_1 { public object? bar(object? x = null) => null; }
class FooType_0 { public FooType_1 Foo = new FooType_1(); }
static FooType_0 foo = new FooType_0();
    public static void Main() {
foo.Foo.bar(ValueTuple.Create(1));
    }
}
