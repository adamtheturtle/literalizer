fn main() {
    struct ThingType;
    impl ThingType { fn Before<A>(&self, _value: A) {} }
    let thing = ThingType;
    thing.Before(1);
}
