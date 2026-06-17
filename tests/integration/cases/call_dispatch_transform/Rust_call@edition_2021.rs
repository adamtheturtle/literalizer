fn main() {
    fn record<A>(_value: A) {}
    fn flush<A>(_count: A) {}
    record(42);
    flush(3);
}
