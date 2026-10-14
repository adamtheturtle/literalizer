fn main() {
    struct ThingType;
    impl ThingType { fn go<A>(&self, _value: A) {} }
    let thing = ThingType;
    let my_data = thing.go(Vec::<String>::new());
    let _ = &my_data;
}
