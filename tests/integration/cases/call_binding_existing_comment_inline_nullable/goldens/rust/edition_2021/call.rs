fn main() {
    fn make_widget<A>(_count: A) {}
    fn consume<A>(_count: A) {}
    let mut my_data = make_widget(None::<()>);
    consume(my_data);
    my_data = make_widget(42); // note
    consume(my_data);
}
