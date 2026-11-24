fn main() {
    fn make_widget<A>(_value: A) {}
    fn wrap_widget<A>(_value: A) {}
    fn consume<A>(_value: A) {}
    let my_data = wrap_widget(
        make_widget(r#"a\ // payload"#) // note
    );
    consume(my_data.clone());
}
