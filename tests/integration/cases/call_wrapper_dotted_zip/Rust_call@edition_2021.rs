fn main() {
    fn process<A>(_value: A) {}
    struct HelpersType;
    impl HelpersType { fn emit<A, B>(&self, __call: A, __zip: B) {} }
    let helpers = HelpersType;
    helpers.emit(process(1), 42);
}
