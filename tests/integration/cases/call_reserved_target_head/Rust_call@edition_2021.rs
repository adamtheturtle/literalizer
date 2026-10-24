fn main() {
    struct ClassType;
    impl ClassType { fn member<A>(&self, _a: A) {} }
    let class = ClassType;
    class.member(42);
}
