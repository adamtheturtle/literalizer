fn main() {
    struct ThingType;
    impl ThingType { fn first_value<A>(&self, _value: A) {} }
    let thing = ThingType;
    thing.first_value(1);
}
