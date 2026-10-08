fn main() {
    struct ThingType_;
    impl ThingType_ { fn go(&self) {} }
    let thing = ThingType_;
    thing.go();
}
