fn main() {
    fn process<A, B>(_data: A, _count: B) {}
    let single_var = vec![
        4,
        5,
        6,
    ];
    let repeated_var = 1;
    process(repeated_var, 1);
    process(single_var, 0);
    process(repeated_var, 8);
}
