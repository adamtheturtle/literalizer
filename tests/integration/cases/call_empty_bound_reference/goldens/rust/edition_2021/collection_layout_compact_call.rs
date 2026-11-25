fn main() {
    fn make_widget<A>(_value: A) {}
    let items = Vec::<String>::new();
    make_widget(items.clone());
}
