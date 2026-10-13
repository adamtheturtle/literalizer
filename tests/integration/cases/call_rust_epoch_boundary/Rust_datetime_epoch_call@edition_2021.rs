fn main() {
    fn consume<A>(_value: A) {}
    consume(-2147483649i64);
    consume(2147483648i64);
}
