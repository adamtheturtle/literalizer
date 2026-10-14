fn main() {
    struct HelperType;
    impl HelperType { fn list<A>(&self, _a: A) {} }
    let helper = HelperType;
    helper.list(1);
}
