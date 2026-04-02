use chrono::NaiveDate;
use chrono::NaiveDateTime;
use chrono::NaiveTime;
fn main() {
    let mut my_data = NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), NaiveTime::from_hms_micro_opt(12, 30, 45, 123456).unwrap());
    my_data = NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), NaiveTime::from_hms_micro_opt(12, 30, 45, 123456).unwrap());
    let _ = my_data;
}
