fn main() {
    fn make_widget<A, B>(_first: A, _second: B) {}
    fn consume<A, B>(_first: A, _second: B) {}
    let my_data = make_widget(42, 3);
    consume(3, my_data.clone());
}
