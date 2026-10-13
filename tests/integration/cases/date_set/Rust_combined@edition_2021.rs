use chrono::NaiveDate;
use std::collections::HashSet;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashSet::from([
        NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(),
        NaiveDate::from_ymd_opt(2024, 6, 1).unwrap(),
    ]);
    let _ = &my_data;
    my_data = HashSet::from([
        NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(),
        NaiveDate::from_ymd_opt(2024, 6, 1).unwrap(),
    ]);
    let _ = &mut my_data;
}
