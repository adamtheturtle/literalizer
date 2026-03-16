use std::collections::HashMap;
use std::collections::HashSet;
fn main() {
    let _ = HashMap::from([
        ("date", NaiveDate::from_ymd_opt(2024, 1, 15).unwrap()),
        ("datetime", NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), NaiveTime::from_hms_opt(12, 30, 0).unwrap())),
    ]);
}
