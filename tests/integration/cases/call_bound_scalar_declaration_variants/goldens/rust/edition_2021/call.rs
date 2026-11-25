fn main() {
    fn consume<A>(_value: A) {}
    let shared = 42;
    consume(shared);
}
