enum Value {
    I32(i32),
    List(Vec<Value>),
}
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
    let my_empty = Vec::<String>::new();
    process(my_ints, 42);
    process(my_strings, 7);
    process(my_empty, 99);
}
