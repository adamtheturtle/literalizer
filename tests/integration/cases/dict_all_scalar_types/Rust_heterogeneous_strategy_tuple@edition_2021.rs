use chrono::NaiveDate;
use chrono::NaiveDateTime;
use chrono::NaiveTime;
use std::collections::HashMap;
struct Record0 {
    s: &'static str,
    i: i32,
    f: f64,
    b: bool,
    n: Option<()>,
    d: NaiveDate,
    dt: NaiveDateTime,
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
        dt: NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), NaiveTime::from_hms_opt(12, 0, 0).unwrap()),
        by: "48656c6c6f",
    };
    let _ = my_data;
}
