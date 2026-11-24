fn main() {
    struct OuterType;
    impl OuterType { fn inner<A, B>(&self, _outer: A, _n: B) {} }
    let outer = OuterType;
    outer.inner(1, 2);
}
