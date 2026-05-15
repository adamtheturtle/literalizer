use chrono::NaiveDate;
use std::collections::HashMap;
struct Record0 {
    s: &'static str,
    i: i32,
    f: f64,
    b: bool,
    n: Option<()>,
    d: NaiveDate,
    dt: i64,
    by: &'static str,
}
fn main() {
    let my_data = Record0 {
        s: "string",
        i: 1,
        f: 1.5,
        b: true,
        n: None::<()>,
        d: NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(),
        dt: 1705320000,
        by: "48656c6c6f",
    };
    let _ = my_data;
}
