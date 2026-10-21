fn main() {
    fn make_widget<A>(_value: A) {}
    let my_data = make_widget(Vec::<String>::new());
    let _ = &my_data;
}
