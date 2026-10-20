fn main() {
    fn consume<A>(_value: A) {}
    let my_null = None::<()>;
    let regular_null = None::<()>;
    consume(my_null);
    consume(regular_null);
}
