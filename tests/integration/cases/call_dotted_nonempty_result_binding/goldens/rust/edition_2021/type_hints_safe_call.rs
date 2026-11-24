fn main() {
    struct ThingType;
    impl ThingType { fn go<A>(&self, _value: A) {} }
    let thing = ThingType;
    let my_data = thing.go(vec![1]);
    let _ = &my_data;
}
