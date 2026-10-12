fn main() {
    fn make_widget<A>(_count: A) {}
    let my_data = make_widget(42) // note
    // extra;
    let _ = my_data;
}
