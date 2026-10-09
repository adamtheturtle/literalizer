fn main() {
    struct ThingType_;
    impl ThingType_ { fn go<A>(&self, _value: A) {} }
    let thing = ThingType_;
    let my_data = thing.go(Vec::<String>::new());
    let _ = my_data;
}
