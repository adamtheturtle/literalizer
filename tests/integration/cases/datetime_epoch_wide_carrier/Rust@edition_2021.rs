use chrono::NaiveDate;
use chrono::NaiveDateTime;
use chrono::NaiveTime;
use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("within_i32", NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), NaiveTime::from_hms_opt(12, 0, 0).unwrap())),
        ("beyond_i32", NaiveDateTime::new(NaiveDate::from_ymd_opt(2099, 6, 15).unwrap(), NaiveTime::from_hms_opt(8, 30, 0).unwrap())),
    ]);
    let _ = my_data;
}
