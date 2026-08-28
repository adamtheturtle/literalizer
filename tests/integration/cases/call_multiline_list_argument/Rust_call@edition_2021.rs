fn main() {
    fn process<A>(_xs: A) {}
    process(vec![
        1,
        2,
    ]);
    process(vec![
        3,
    ]);
}
