fn main() {
    fn consume<A>(_value: A) {}
    static SHARED: i32 = 42;
    consume(SHARED);
}
