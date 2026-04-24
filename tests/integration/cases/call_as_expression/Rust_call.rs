fn main() {
    fn process<A, B>(_a: A, _b: B) {}
    let items = vec![
        process(1, 42),
        process(2, 100),
    ];
    let _ = items;
}
