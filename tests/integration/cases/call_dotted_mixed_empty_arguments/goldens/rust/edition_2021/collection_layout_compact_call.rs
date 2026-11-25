fn main() {
    struct ThingType;
    impl ThingType { fn go<A, B, C>(&self, _before: A, _populated: B, _after: C) {} }
    let thing = ThingType;
    thing.go(Vec::<String>::new(), vec![1], Vec::<String>::new());
    thing.go(vec!["text"], vec![2], Vec::<String>::new());
    thing.go(Vec::<String>::new(), vec!["text"], Vec::<String>::new());
    thing.go(vec!["text"], vec![2], vec![3]);
}
