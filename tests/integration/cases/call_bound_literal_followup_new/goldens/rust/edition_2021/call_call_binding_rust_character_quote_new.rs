fn main() {
    fn make_widget<A>(_value: A) {}
    fn consume<A>(_value: A) {}
    let my_data = make_widget('"'); // note
    consume(my_data.clone());
}
