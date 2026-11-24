fn main() {
    struct FooType;
    impl FooType { fn class<A>(&self, _value: A) {} }
    let foo = FooType;
    foo.class(1);
}
