fn main() {
    struct ThingType;
    impl ThingType { fn go<A>(&self, _value: A) {} }
    let thing = ThingType;
    let item = vec![
        1,
        2,
    ];
    thing.go(item.clone());
}
