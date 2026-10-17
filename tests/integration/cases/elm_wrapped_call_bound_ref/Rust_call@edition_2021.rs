fn main() {
    fn make_widget<A>(_value: A) {}
    let value = 1;
    make_widget(value);
}
