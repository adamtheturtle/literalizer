fn main() {
    fn raw_value<A>(_value: A) {}
    fn consume<A>(_value: A) {}
    let my_data = raw_value(42); // note
    consume(my_data.clone());
}
