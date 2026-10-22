fn main() {
    fn consume<A>(_value: A) {}
    let item = vec![
        1,
        2,
    ];
    consume(item);
}
