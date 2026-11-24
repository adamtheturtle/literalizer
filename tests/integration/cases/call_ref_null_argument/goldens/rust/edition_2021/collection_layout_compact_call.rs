fn main() {
    fn consume<A>(_value: A) {}
    let value = None::<()>;
    consume(value);
}
