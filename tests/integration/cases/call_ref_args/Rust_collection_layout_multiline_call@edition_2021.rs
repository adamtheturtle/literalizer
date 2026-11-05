fn main() {
    fn process<A, B>(_data: A, _count: B) {}
    let my_var = vec![
        1,
        2,
        3,
    ];
    let my_other = vec![
        4,
        5,
        6,
    ];
    process(my_var, 42);
    process(my_other, 7);
}
