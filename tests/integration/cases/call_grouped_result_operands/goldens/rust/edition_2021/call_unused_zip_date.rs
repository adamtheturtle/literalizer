fn main() {
    fn make_widget<A>(_count: A) {}
    fn wrap_widget<A, B>(_value: A, _extra: B) {}
    fn consume<A>(_count: A) {}
    let my_data = {
        wrap_widget(make_widget(42), r#"// group"#)
    };
    consume(my_data.clone());
}
