fn main() {
    fn make_widget<A>(_value: A) {}
    let my_data = make_widget(vec![1]);
    let _ = &my_data;
}
