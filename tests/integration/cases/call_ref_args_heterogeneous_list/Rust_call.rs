fn main() {
    fn process<A, B>(_data: A, _count: B) {}
    let my_ints = vec![
        1,
        2,
        3,
    ];
    let my_strings = vec![
        "a",
        "b",
    ];
    process(my_ints, 42);
    process(my_strings, 7);
}
