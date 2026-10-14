use chrono::NaiveDate;
use std::collections::HashMap;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        (NaiveDate::from_ymd_opt(2024, 1, 1).unwrap(), "new_year"),
        (NaiveDate::from_ymd_opt(2024, 7, 4).unwrap(), "independence_day"),
        (NaiveDate::from_ymd_opt(2024, 12, 25).unwrap(), "christmas"),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        (NaiveDate::from_ymd_opt(2024, 1, 1).unwrap(), "new_year"),
        (NaiveDate::from_ymd_opt(2024, 7, 4).unwrap(), "independence_day"),
        (NaiveDate::from_ymd_opt(2024, 12, 25).unwrap(), "christmas"),
    ]);
    let _ = &mut my_data;
}
