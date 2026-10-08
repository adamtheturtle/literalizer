fn main() {
    struct FooType_;
    impl FooType_ { fn class<A>(&self, _value: A) {} }
    let foo = FooType_;
    foo.class(1);
}
