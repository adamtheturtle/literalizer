fn main() {
    struct ThingType_;
    impl ThingType_ { fn go<A>(&self, _value: A) {} }
    let thing = ThingType_;
    let item = vec![
        1,
        2,
    ];
    thing.go(item);
}
