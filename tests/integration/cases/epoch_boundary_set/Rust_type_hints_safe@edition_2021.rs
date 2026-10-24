use chrono::NaiveDate;
use chrono::NaiveDateTime;
use chrono::NaiveTime;
use std::collections::HashSet;
fn main() {
    let my_data = HashSet::from([
        NaiveDateTime::new(NaiveDate::from_ymd_opt(1901, 12, 13).unwrap(), NaiveTime::from_hms_opt(20, 45, 51).unwrap()),
        NaiveDateTime::new(NaiveDate::from_ymd_opt(1901, 12, 13).unwrap(), NaiveTime::from_hms_opt(20, 45, 52).unwrap()),
        NaiveDateTime::new(NaiveDate::from_ymd_opt(2038, 1, 19).unwrap(), NaiveTime::from_hms_opt(3, 14, 7).unwrap()),
        NaiveDateTime::new(NaiveDate::from_ymd_opt(2038, 1, 19).unwrap(), NaiveTime::from_hms_opt(3, 14, 8).unwrap()),
    ]);
    let _ = &my_data;
}
