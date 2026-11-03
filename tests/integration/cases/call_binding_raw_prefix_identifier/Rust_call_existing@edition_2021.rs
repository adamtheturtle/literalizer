fn main() {
    fn raw_value<A>(_value: A) {}
    fn consume<A>(_value: A) {}
    let mut my_data = raw_value(42);
    consume(my_data);
    my_data = raw_value(42); // note
    consume(my_data);
}
