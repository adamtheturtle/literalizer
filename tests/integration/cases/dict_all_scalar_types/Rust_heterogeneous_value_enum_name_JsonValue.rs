use chrono::NaiveDate;
use chrono::NaiveDateTime;
use chrono::NaiveTime;
use std::collections::HashMap;
enum JsonValue {
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
        ("s", JsonValue::Str("string")),
        ("i", JsonValue::I32(1)),
        ("f", JsonValue::F64(1.5)),
        ("b", JsonValue::Bool(true)),
        ("n", JsonValue::Null),
        ("d", JsonValue::Date(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap())),
        ("dt", JsonValue::DateTime(NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), NaiveTime::from_hms_opt(12, 0, 0).unwrap()))),
        ("by", JsonValue::Bytes("48656c6c6f")),
    ]);
    let _ = my_data;
}
