fn main() {
    struct ThingType;
    impl ThingType { fn go<A, B, C>(&self, _before: A, _populated: B, _after: C) {} }
    let thing = ThingType;
    thing.go([] as [String; 0], [1], [] as [String; 0]);
    thing.go(["text"], [2], [] as [String; 0]);
    thing.go([] as [String; 0], ["text"], [] as [String; 0]);
    thing.go(["text"], [2], [3]);
}
