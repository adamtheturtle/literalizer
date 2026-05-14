enum Value {
    Bool(bool),
    I32(i32),
    F64(f64),
}
fn main() {
    fn process<A, B>(_value: A, _count: B) {}
    let my_int = 1;
    let my_bool = true;
    let my_float = 3.14;
    let my_list = vec![
        1,
        2,
        3,
    ];
    process(my_int, 42);
    process(my_bool, 7);
    process(my_float, 9);
    process(my_list, 1);
}
