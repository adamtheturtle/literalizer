fn main() {
    fn make_widget<A>(_value: A) {}
    fn consume<A>(_value: A) {}
    let my_data = make_widget('\x2f'); // note
    consume(my_data);
}
