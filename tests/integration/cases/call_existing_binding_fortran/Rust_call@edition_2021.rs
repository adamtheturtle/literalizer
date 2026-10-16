fn main() {
    fn make_widget<A>(_count: A) {}
    let mut my_data = make_widget(0);
    my_data = make_widget(1);
}
