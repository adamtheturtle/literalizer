fn main() {
    struct ClassType_;
    impl ClassType_ { fn member<A>(&self, _a: A) {} }
    let class = ClassType_;
    class.member(42);
}
