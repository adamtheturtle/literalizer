use chrono::NaiveDate;
use std::collections::BTreeSet;
fn main() {
    let my_data = BTreeSet::from([
        NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(),
        NaiveDate::from_ymd_opt(2024, 6, 1).unwrap(),
    ]);
    let _ = &my_data;
}
