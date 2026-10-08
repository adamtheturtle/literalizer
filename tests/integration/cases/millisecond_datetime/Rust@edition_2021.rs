use chrono::NaiveDate;
use chrono::NaiveDateTime;
use chrono::NaiveTime;
use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("half", NaiveDateTime::new(NaiveDate::from_ymd_opt(1979, 5, 27).unwrap(), NaiveTime::from_hms_micro_opt(7, 32, 0, 500000).unwrap())),
        ("milli", NaiveDateTime::new(NaiveDate::from_ymd_opt(1979, 5, 27).unwrap(), NaiveTime::from_hms_micro_opt(7, 32, 0, 100000).unwrap())),
        ("max_milli", NaiveDateTime::new(NaiveDate::from_ymd_opt(1979, 5, 27).unwrap(), NaiveTime::from_hms_micro_opt(7, 32, 0, 999000).unwrap())),
        ("whole", NaiveDateTime::new(NaiveDate::from_ymd_opt(1979, 5, 27).unwrap(), NaiveTime::from_hms_opt(7, 32, 0).unwrap())),
    ]);
    let _ = my_data;
}
