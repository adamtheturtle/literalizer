fn main() {
    fn consume<A>(_value: A) {}
    let external_value = 1;
    consume(external_value);
}
