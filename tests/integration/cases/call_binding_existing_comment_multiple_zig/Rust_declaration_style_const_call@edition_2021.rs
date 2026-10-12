fn main() {
    fn make_widget<A>(_count: A) {}
    const my_data: i32 = 42;
    my_data = make_widget(42) // note
    // extra;
}
