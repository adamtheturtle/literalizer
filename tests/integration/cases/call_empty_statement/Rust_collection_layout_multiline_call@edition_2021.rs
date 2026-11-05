fn main() {
    fn make_widget<A>(_value: A) {}
    make_widget(Vec::<String>::new());
}
