use chrono::NaiveDate;
fn main() {
    fn capture<A, B, C, D, E, F, G>(_nan_value: A, _positive_infinity: B, _negative_infinity: C, _finite_value: D, _date_value: E, _datetime_value: F, _text_value: G) {}
    capture(f64::NAN, f64::INFINITY, f64::NEG_INFINITY, 1.25, NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), 1705322096, "[ordinary text]");
}
