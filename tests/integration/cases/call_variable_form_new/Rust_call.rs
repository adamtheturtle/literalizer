fn main() {
    fn make_widget<A>(_count: A) {}
    let result = make_widget(42);
    let _ = result;
}
