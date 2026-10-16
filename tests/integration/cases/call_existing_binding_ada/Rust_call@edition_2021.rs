fn main() {
    fn make_widget<A>(_count: A) {}
    let mut my_data = make_widget(0);
    make_widget(my_data);
    my_data = make_widget(1);
    make_widget(my_data);
}
