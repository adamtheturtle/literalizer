use chrono::NaiveDate;
use chrono::NaiveDateTime;
use chrono::NaiveTime;
fn main() {
    let my_data = vec![
        NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), NaiveTime::from_hms_micro_opt(12, 30, 0, 123456).unwrap()),
        NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 6, 1).unwrap(), NaiveTime::from_hms_opt(8, 0, 0).unwrap()),
    ];
    let _ = my_data;
}
