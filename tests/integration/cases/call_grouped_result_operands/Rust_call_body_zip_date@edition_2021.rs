use chrono::NaiveDate;
fn main() {
    fn make_widget<A>(_count: A) {}
    fn wrap_widget<A, B>(_value: A, _extra: B) {}
    fn zip_widget<A, B>(_value: A, _extra: B) {}
    fn consume<A>(_count: A) {}
    let my_data = wrap_widget({
        zip_widget(make_widget(42), NaiveDate::from_ymd_opt(2024, 1, 15).unwrap())
    }, r#"// group"#);
    consume(my_data.clone());
}
