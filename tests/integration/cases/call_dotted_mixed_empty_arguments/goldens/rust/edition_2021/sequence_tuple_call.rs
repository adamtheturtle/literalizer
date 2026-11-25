fn main() {
    struct ThingType;
    impl ThingType { fn go<A, B, C>(&self, _before: A, _populated: B, _after: C) {} }
    let thing = ThingType;
    thing.go((), (1,), ());
    thing.go(("text",), (2,), ());
    thing.go((), ("text",), ());
    thing.go(("text",), (2,), (3,));
}
