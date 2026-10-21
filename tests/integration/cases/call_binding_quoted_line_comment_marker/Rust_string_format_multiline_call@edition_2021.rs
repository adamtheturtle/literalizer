fn main() {
    fn make_widget<A>(_text: A) {}
    let my_data = make_widget(r#"first "quote"
// string body"#); // note
    // extra
    let _ = &my_data;
}
