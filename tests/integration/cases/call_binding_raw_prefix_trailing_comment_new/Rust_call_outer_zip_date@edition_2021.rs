use chrono::NaiveDate;
fn main() {
    fn make_widget<A>(_value: A) {}
    fn wrap_widget<A, B>(_value: A, _zipped: B) {}
    fn consume<A>(_value: A) {}
    let my_data = wrap_widget(
        make_widget(r#"a\ // payload"#) // note
        , NaiveDate::from_ymd_opt(2024, 1, 15).unwrap()
    );
    consume(my_data.clone());
}
