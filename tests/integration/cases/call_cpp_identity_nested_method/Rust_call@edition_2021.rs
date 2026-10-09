fn main() {
    struct ThingType_;
    impl ThingType_ { fn go(&self) {} }
    struct OuterType_ { thing: ThingType_ }
    let outer = OuterType_ { thing: ThingType_ };
    outer.thing.go();
}
