fn main() {
    fn make_widget<A>(_value: A) {}
    fn consume<A>(_value: A) {}
    let my_data = make_widget(42);
    consume(my_data.clone());
}
