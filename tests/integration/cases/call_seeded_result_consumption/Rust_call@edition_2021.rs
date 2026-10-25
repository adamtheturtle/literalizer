fn main() {
    fn make_widget<A>(_count: A) {}
    fn consume_widget<A>(_count: A) {}
    let mut my_data = make_widget(0);
    consume_widget(my_data);
    my_data = make_widget(1);
    consume_widget(my_data);
}
