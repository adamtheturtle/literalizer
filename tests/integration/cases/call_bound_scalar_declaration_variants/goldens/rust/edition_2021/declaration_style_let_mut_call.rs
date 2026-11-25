fn main() {
    fn consume<A>(_value: A) {}
    let mut shared = 42;
    let _ = &mut shared;
    consume(shared);
}
