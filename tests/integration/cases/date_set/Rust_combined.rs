use chrono::NaiveDate;
use std::collections::HashSet;
fn main() {
    let mut my_data = HashSet::from([
        NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(),
        NaiveDate::from_ymd_opt(2024, 6, 1).unwrap(),
    ]);
    my_data = HashSet::from([
        NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(),
        NaiveDate::from_ymd_opt(2024, 6, 1).unwrap(),
    ]);
    let _ = my_data;
}
