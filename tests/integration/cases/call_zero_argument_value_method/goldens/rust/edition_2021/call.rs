fn main() {
    struct ThingType;
    impl ThingType { fn go(&self) {} }
    let thing = ThingType;
    thing.go();
}
