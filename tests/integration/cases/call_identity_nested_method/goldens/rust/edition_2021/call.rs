fn main() {
    struct ThingType;
    impl ThingType { fn go(&self) {} }
    struct OuterType { thing: ThingType }
    let outer = OuterType { thing: ThingType };
    outer.thing.go();
}
