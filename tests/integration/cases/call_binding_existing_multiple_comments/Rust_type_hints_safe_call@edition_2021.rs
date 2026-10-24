fn main() {
    fn make_widget<A>(_count: A) {}
    fn consume_widget<A>(_count: A) {}
    let mut my_data = make_widget(42);
    consume_widget(my_data);
    my_data = make_widget(42); // note
    // extra
    consume_widget(my_data);
}
