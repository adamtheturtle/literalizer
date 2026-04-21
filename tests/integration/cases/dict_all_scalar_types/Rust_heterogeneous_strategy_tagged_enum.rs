use chrono::NaiveDate;
use chrono::NaiveDateTime;
use chrono::NaiveTime;
use std::collections::HashMap;
enum Value {
    Str(&'static str),
    I32(i32),
    F64(f64),
    Bool(bool),
    Null,
    Date(NaiveDate),
    DateTime(NaiveDateTime),
    Bytes(&'static str),
}
fn main() {
    let my_data = HashMap::from([
        ("s", Value::Str("string")),
        ("i", Value::I32(1)),
        ("f", Value::F64(1.5)),
        ("b", Value::Bool(true)),
        ("n", Value::Null),
        ("d", Value::Date(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap())),
        ("dt", Value::DateTime(NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), NaiveTime::from_hms_opt(12, 0, 0).unwrap()))),
        ("by", Value::Bytes("48656c6c6f")),
    ]);
    let _ = my_data;
}
