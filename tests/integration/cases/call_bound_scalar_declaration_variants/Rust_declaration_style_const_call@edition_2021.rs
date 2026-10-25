fn main() {
    fn consume<A>(_value: A) {}
    const SHARED: i32 = 42;
    consume(SHARED);
}
