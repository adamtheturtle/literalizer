fn main() {
    fn make_widget<A>(_count: A) {}
    let my_data = make_widget(42) ?
    make_widget(42) // inner
    : nil // trailing;
    let _ = my_data;
}
