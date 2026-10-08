fn main() {
    struct OuterType_;
    impl OuterType_ { fn inner<A, B>(&self, _outer: A, _n: B) {} }
    let outer = OuterType_;
    outer.inner(1, 2);
}
