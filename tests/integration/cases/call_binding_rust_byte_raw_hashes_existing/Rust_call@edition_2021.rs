fn main() {
    fn make_widget<A>(_value: A) {}
    fn consume<A>(_value: A) {}
    let mut my_data = make_widget(42);
    consume(my_data);
    my_data = make_widget(br#"// payload"#); // note
    consume(my_data);
}
