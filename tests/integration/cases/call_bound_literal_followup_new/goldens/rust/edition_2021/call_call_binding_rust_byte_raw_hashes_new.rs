fn main() {
    fn make_widget<A>(_value: A) {}
    fn consume<A>(_value: A) {}
    let my_data = make_widget(br#"// payload"#); // note
    consume(my_data.clone());
}
