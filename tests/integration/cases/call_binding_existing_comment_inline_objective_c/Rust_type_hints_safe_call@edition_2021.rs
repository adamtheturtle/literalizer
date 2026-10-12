fn main() {
    fn make_widget<A>(_count: A) {}
    let my_data = 42;
    my_data = make_widget(my_data) // note;
    make_widget(my_data);
}
