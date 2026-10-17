fn main() {
    fn make_widget<A, B>(_first_value: A, _second_value: B) {}
    make_widget(vec![1], vec!["text"]);
}
