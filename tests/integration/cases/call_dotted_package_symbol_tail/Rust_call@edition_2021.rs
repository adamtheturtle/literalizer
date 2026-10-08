fn main() {
    struct HelperType_;
    impl HelperType_ { fn list<A>(&self, _a: A) {} }
    let helper = HelperType_;
    helper.list(1);
}
